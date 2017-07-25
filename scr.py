import numpy as np
from threading import Timer
import scipy.stats as scistats
import sys
import os

class Snake_Searcher:
    """"

    Snake_Searcher groups data based on the chi-squared statistical test.

        Test Failed: Append new value to group, removing first value.
        Test Passed: Export group, start new group with next value.
        *Note* Minimum group value must not be smaller than 5 otherwise the
                chi-squared test becomes unreliable.

    """
    def __init__(self, *data_list, length=10, start=0, chi_tol=0.9995,
                 verbose=True):
        length_trigger = bool
        self.log = Print_Log(verbose)
        self.log.print_it("*** SNAKE SEARCHER ***")
        self.log.print_it("SS: Initialising Snake_Searcher.")
        self.data_list = [x for x in data_list]
        self.length = length
        self.log.print_it("    Specified sublist length:",
                            self.length)
        if self.length >= 5:
            length_trigger = True
        self.chi_tol = chi_tol
        self.log.print_it("    Chi-squared statistic tolerance: p =",
                            self.chi_tol)
        self.output = {}
        if length_trigger:
            self.main_loop()
        else:
            print("SS: Sublist length too short. Consult docstring.")

    def main_loop(self):
        self.log.print_it("    Proceeding to analyse input list.")
        counter = 1
        for lst in self.data_list:
            first = True
            self.list_to_analyse = lst
            # listname = input("<<Please Enter Data Set Name>>\n")
            listname = counter
            counter += 1
            self.output[str(listname)] = []
            while True:
                self.snake = []
                if first:
                    finished = self.snake_moves()
                    total_snake = self.snake_grows()
                    first = False
                    self.output[str(listname)].append(total_snake)
                else:
                    finished = self.snake_moves(start=self.current)
                    if finished:
                        self.log.print_it("SS: Data set", listname,
                                            "analysis completed.")
                        break
                    total_snake = self.snake_grows()
                    self.output[str(listname)].append(total_snake)
            if len(self.output) == len(self.data_list):
                self.log.print_it(
                        "SS: Your data can be accessed by the method - "
                        "[object.SS_output()]:")
                self.log.print_it("*** SNAKE SEARCH TERMINATED ***\n")
                break

    def snake_moves(self, start=0):
        self.current = start
        while True:
            if self.current == len(self.list_to_analyse):
                if len(self.snake) >= 5:
                    if self.snake_is_flat(bypass=True):
                        return True
                return True
            if len(self.snake) > self.length:
                self.log.print_it("SS: Removing", self.snake[0],
                                    "from test array.")
                del self.snake[0]
            if self.snake_is_flat():
                self.log.print_it("SS: Current sublist", self.snake,
                      "satisfies convergence.\n\tGrowing...\n")
                return False
            self.log.print_it("    Starting position in parent list:",
                                self.current,"\n")
            self.snake.append(float(self.list_to_analyse[self.current]))
            self.log.print_it("SS: Appending next value",
                                float(self.list_to_analyse[self.current]),
                                "to sublist.")
            self.current += 1

    def snake_is_flat(self, bypass=False):
        if len(self.snake) >= self.length or bypass:
            self.log.print_it("SS: Equilibrium test:")
            self.snake_check_array = np.array(self.snake)
            self.log.print_it("    Test array:", str(self.snake))
            self.log.print_it("    Testing array chi-squared statistic.")
            chisq, p = scistats.chisquare(self.snake)
            self.log.print_it("    Chi-squared test statistic:", chisq)
            if p > self.chi_tol:
                self.log.print_it("    Probablility:", p, ">",
                                    self.chi_tol, "tolerance.")
                self.log.print_it("    Accepted.\n")
                return True
            else:
                self.log.print_it("    Probablility:", p, "<",
                                    self.chi_tol, "tolerance.")
                self.log.print_it("    Rejected.\n")
                return False
        else:
            return False

    def snake_grows(self):
        while True:
            if self.current == len(self.list_to_analyse):
                self.log.print_it("SS: No more data, halting growth.")
                return self.snake
            self.snake.append(float(self.list_to_analyse[self.current]))
            self.log.print_it("SS: Appending next value",
                                float(self.list_to_analyse[self.current]),
                                "to sublist.")
            chisq, p = scistats.chisquare(self.snake)
            if p > self.chi_tol:
                self.log.print_it("    Probablility:", p, ">",
                                    self.chi_tol, "tolerance.")
                self.log.print_it("    Growing...\n")
                self.current += 1
            else:
                self.log.print_it("    Probablility:", p, "<",
                                    self.chi_tol, "tolerance.")
                self.log.print_it("    Fully grown.\n")
                del self.snake[-1]
                self.snake = np.asarray(self.snake)
                self.snake = self.reject_outliers(self.snake)
                return self.snake

    def reject_outliers(self, data, m = 3):
        deviation = np.abs(data - np.median(data))
        median_absolute_deviation = np.median(deviation)
        s = deviation/median_absolute_deviation if median_absolute_deviation else 0
        return data[s<m]

    def SS_output(self):
        return self.output

class Data_Chomper:
    def __init__(self, grouped_data, verbose=True):
        self.log = Print_Log(verbose)
        self.log.print_it("*** DATA CHOMPER ***")
        self.log.print_it("DC: Initialising Data_Chomper.")
        self.input = grouped_data
        self.output = {}
        self.log.print_it("DC: Executing main function.")
        self.main_loop()

    def main_loop(self):
        if type(self.input) == dict:
            self.log.print_it("DC: Data identified as dictionary.")
            for key in self.input.keys():
                self.log.print_it("DC: Packing data in dictionary key ", key)
                self.pack_groups(self.input[key], key)
        if type(self.input) == list:
            self.log.print_it("DC: Data identified as list.")
            listnumber = 1
            for data in self.input:
                self.log.print_it("DC: Packing list number", listnumber,
                                  listnumber)
                self.pack_groups(data)
                listnumber += 1

    def pack_groups(self, data, index):
        self.output[index] = []
        for array in data:
            self.output[index].append((np.average(array), np.std(array), len(array)))
#     def pack_groups(self, data):
#         for grp_no in range(len(data)):
#             if grp_no == 0:
#                 current_grp = np.array(data[grp_no])
#                 next_grp = np.array(data[grp_no + 1])
#                 cond = (np.average(current_grp) - np.average(next_grp)) < 15
#                 if cond:
#                     self.builder.append(current_grp)
#                     self.builder.append(next_grp)
#                 else:
#                     self.output.append(self.current_grp)
#             elif grp_no < len(data) - 1:
#                 current_grp = np.array(data[grp_no])
#                 next_grp = np.array(data[grp_no + 1])
#                 cond = (abs(np.average(current_grp) -
#                             np.average(next_grp)) < 15)
#                 if cond:
#                     self.builder.append(next_grp)
#                 else:
#                     if len(self.builder) == 0:
#                         pass
#                     else:
#                         self.output.append(self.builder)
#                         self.builder = []
#             else:
#                 current_grp = np.array(data[grp_no])
#                 prev_grp = np.array(data[grp_no - 1])
#                 cond = (abs(np.average(current_grp) -
#                             np.average(prev_grp)) < 15)
#                 if cond:
#                     self.builder.append(current_grp)
#                     self.output.append(self.builder)
#                 else:
#                     self.output.append(self.builder)
#                     self.output.append(current_grp)
#         for sets in self.output:
#             lists = np.array([j for i in sets for j in i])
#             self.points.append((np.average(lists), np.std(lists),
#                                 len(lists)))
#
#     def DC_output(self):
#         return self.points
#
#
# class Rebuilder:
#     def __init__(self, reservoir, sample):
#         self.reservoir = reservoir
#         self.sample = sample
#         self.r_start = 0
#         self.startlist = []
#         self.linklist = []
#         self.outlist = []
#
#     def rebuildit(self):
#         for sdata in self.sample:
#             for rdata in self.reservoir:
#                 if ((abs(sdata[0] - rdata[0]) < 15) and
#                         (self.reservoir.index(rdata) >= self.r_start)):
#                     self.r_start = self.reservoir.index(rdata)
#                     self.startlist.append(self.r_start)
#                     self.linklist.append((sdata[0], rdata[0]))
#
#                     break
#         c = 0
#         for val in range(len(self.reservoir)):
#             if val in self.startlist:
#                 self.outlist.append(self.linklist[c])
#                 c += 1
#             else:
#                 self.outlist.append(self.reservoir[val][0])
#
#     def give_data(self):
#         return self.outlist

class Print_Log:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def print_it(self, *string):
        words = [str(x) for x in string]
        if self.verbose:
            first = True
            for word in words:
                if first:
                    print('\n', word, end=' ')
                    first = False
                else:
                    print(word, end=' ')

        else:
            pass
