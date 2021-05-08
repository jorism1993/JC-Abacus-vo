import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
from typing import List

PATH_NAME = os.path.join('Chat export 31-12-2020', 'export.txt')


class Message:

    def __init__(self, line):
        self.line = line

        try:
            self.time = line.split(' - ')[0]
            self.time = datetime.strptime(self.time, '%d-%m-%Y %H:%M')

            self.sender = ''.join(line.split(' - ')[1:]).split(':')[0]
            self.content = ''.join(''.join(line.split(' - ')[1:]).split(':')[1:]).lower()

            self.correct = any(s in self.content for s in
                               ['vo', 'voo', 'braveau', 'veau', 'bvo', 'bravo', 'vooo', 'voooo', 'vooooo']) and \
                           self.time.hour == 12 and self.time.minute == 13

            self.incorrect = any(s in self.content for s in
                                 ['vo', 'voo', 'braveau', 'veau', 'bvo', 'bravo', 'vooo', 'voooo', 'vooooo',
                                  'Dit bericht is verwijderd']) and \
                             self.time.hour == 12 and (self.time.minute == 12 or self.time.minute == 14)

            self.valid = True

        except:
            self.valid = False


def load_data(path: str):
    """ Load the data into a list of instances of the message class """

    with open(path, 'r', encoding='utf-8') as export_file:
        lines = export_file.readlines()

    messages = [Message(line) for line in lines]
    all_messages = [message for message in messages if message.valid]
    return all_messages


def plot_all_time(messages: List[Message]):
    """ Make a plot of the most correct messages of a year """
    filtered_messages = [message for message in messages]

    data_correct, data_incorrect = defaultdict(int), defaultdict(int)

    for message in filtered_messages:

        if message.correct:
            data_correct[message.sender] += 1
        elif message.incorrect:
            data_incorrect[message.sender] += 1

    data_correct = [(person, count) for (person, count) in data_correct.items()]
    data_correct = list(reversed(sorted(data_correct, key=lambda x: x[1])))

    data_incorrect = [(person, count) for (person, count) in data_incorrect.items()]
    data_incorrect = list(reversed(sorted(data_incorrect, key=lambda x: x[1])))

    plt.figure(figsize=(20, 10))
    plt.bar(*zip(*data_correct))
    plt.xticks(rotation=35, fontsize=25, ha='right')
    plt.yticks(fontsize=25)
    plt.title(f'Aantal keer vo sinds 26-03-2016', fontsize=35)
    plt.tight_layout()
    plt.savefig('all_time_correct.png')
    plt.close()

    plt.figure(figsize=(20, 10))
    plt.bar(*zip(*data_incorrect))
    plt.xticks(rotation=35, fontsize=25, ha='right')
    plt.yticks(fontsize=25)
    plt.title(f'Aantal keer vo om 12:12 of 12:14 sinds 26-03-2016', fontsize=35)
    plt.tight_layout()
    plt.savefig('all_time_incorrect.png')
    plt.close()

    return


def plot_year(messages: List[Message], year: int = 2016):
    """ Make a plot of the most correct messages of a year """
    filtered_messages = [message for message in messages if message.time.year == year]

    data_correct, data_incorrect = defaultdict(int), defaultdict(int)

    for message in filtered_messages:

        if message.correct:
            data_correct[message.sender] += 1
        elif message.incorrect:
            data_incorrect[message.sender] += 1

    data_correct = [(person, count) for (person, count) in data_correct.items()]
    data_correct = list(reversed(sorted(data_correct, key=lambda x: x[1])))
    correct_labels = [f'{count}' for (name, count) in data_correct]

    data_incorrect = [(person, count) for (person, count) in data_incorrect.items()]
    data_incorrect = list(reversed(sorted(data_incorrect, key=lambda x: x[1])))
    incorrect_labels = [f'{count}' for (name, count) in data_incorrect]

    plt.figure(figsize=(20, 10))
    plt.bar(*zip(*data_correct), label=correct_labels)
    plt.xticks(rotation=35, fontsize=25, ha='right')
    plt.yticks(fontsize=25)
    plt.title(f'Aantal keer vo in {year}', fontsize=35)
    for (name, count), label in zip(data_correct, correct_labels):
        plt.text(name, count, str(label))
    plt.tight_layout()
    plt.savefig(f'{year}_correct.png')
    plt.close()

    plt.figure(figsize=(20, 10))
    plt.bar(*zip(*data_incorrect))
    plt.xticks(rotation=35, fontsize=25, ha='right')
    plt.yticks(fontsize=25)
    plt.title(f'Aantal keer vo om 12:12 of 12:14 in {year}', fontsize=35)
    for (name, count), label in zip(data_incorrect, incorrect_labels):
        plt.text(name, count, str(label))
    plt.tight_layout()
    plt.savefig(f'{year}_incorrect.png')
    plt.close()

    return


def plot_diff(messages: List[Message], min_year: int, max_year: int):
    """ Plot the relative difference between two years"""

    assert min_year < max_year, "Years not valid"

    min_messages = [message for message in messages if message.time.year == min_year]
    max_messages = [message for message in messages if message.time.year == max_year]

    min_data, max_data, diff_data = defaultdict(int), defaultdict(int), defaultdict(float)

    for message in min_messages:
        if message.correct:
            min_data[message.sender] += 1

    for message in max_messages:
        if message.correct:
            max_data[message.sender] += 1

    for key in min_data.keys():
        diff_data[key] = 100. * (max_data[key] - min_data[key]) / float(min_data[key])

    diff_data = [(person, count) for (person, count) in diff_data.items()]
    diff_data = list(reversed(sorted(diff_data, key=lambda x: x[1])))
    diff_data_labels = [f'{round(count, 2)}%' for (name, count) in diff_data]

    colours = []
    for person, count in diff_data:
        if count < 0:
            colours.append('r')
        else:
            colours.append('g')

    plt.figure(figsize=(20, 10))
    plt.bar(*zip(*diff_data), color=colours)
    plt.xticks(rotation=35, fontsize=25, ha='right')
    plt.yticks(fontsize=25)
    plt.title(f'Procentuele verandering tussen {min_year} en {max_year}', fontsize=35)
    for (name, count), label in zip(diff_data, diff_data_labels):
        plt.text(name, count, str(label))
    plt.tight_layout()
    plt.savefig(f'change_{min_year}_{max_year}.png')
    plt.close()


if __name__ == '__main__':
    messages = load_data(PATH_NAME)
    # plot_year(messages, year=2016)
    # plot_year(messages, year=2017)
    # plot_year(messages, year=2018)
    plot_year(messages, year=2019)
    plot_year(messages, year=2020)

    # plot_all_time(messages)
    plot_diff(messages, 2019, 2020)
