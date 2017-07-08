import sys, argparse
import pandas as pd
 
precision = 3
nth = 3
#colors = ["{\cellcolor{green!20}}","{\cellcolor{orange!20}}","{\cellcolor{yellow!20}}"]
colors = ["{\cellcolor{blue!20}}","{\cellcolor{green!20}}","{\cellcolor{yellow!20}}"]
smallest = False
fulldocument = False

def create_header(data_frame, number_of_columns):
    rows_string = ''
    if fulldocument:
        rows_string = r'\documentclass[landscape]{article}' + '\n' + r'\usepackage{xcolor}' + '\n' + r'\usepackage{colortbl}' + '\n' + r'\begin{document}' + '\n'
        rows_string = rows_string + r'\noindent\makebox[\textwidth]{' +'\n'
    rows_string = rows_string + r'\begin{tabular}{' + '|c' * number_of_columns + '|}\n' + '\\hline \n'
    rows_string = rows_string + " & ".join(data_frame.columns.values.tolist()) + r'\\ ' + '\hline \n'
    return rows_string

def get_nth_largest_values(data_frame, dataset, nth, number_of_columns):
    nlargestValues = pd.to_numeric(data_frame.iloc[dataset][1:]).nlargest(nth).unique()
    count = nth
    while len(nlargestValues) != nth and count <= number_of_columns:
        count = count + 1
        nlargestValues = pd.to_numeric(data_frame.iloc[dataset][1:]).nlargest(count).unique()
    return nlargestValues

def get_nth_smallest_values(data_frame, dataset, nth, number_of_columns):
    nsmallestValues = pd.to_numeric(data_frame.iloc[dataset][1:]).nsmallest(nth).unique()
    count = nth
    while len(nsmallestValues) != nth and count <= number_of_columns:
        count = count + 1
        nsmallestValues = pd.to_numeric(data_frame.iloc[dataset][1:]).nsmallest(count).unique()
    return nsmallestValues

def get_latex_string(data_frame, nth):
    number_of_columns = len(data_frame.columns)
    rows_string = create_header(data_frame, number_of_columns)
    for dataset in range(number_of_columns):
        if smallest:
            nValues = get_nth_smallest_values(data_frame, dataset, nth, number_of_columns)
        else:
            nValues = get_nth_largest_values(data_frame, dataset, nth, number_of_columns)
        for value in range(len(data_frame.iloc[dataset])):
            delimiter_char = r' & '
            if value == len(data_frame.iloc[dataset]) -1:
                delimiter_char = r'\\' + '\n'
            if value==0:
                rows_string = rows_string + data_frame.iloc[dataset][value] + delimiter_char
            else:
                cellvalue = data_frame.iloc[dataset][value]
                extreme_value = False
                for i in range(len(nValues)):
                    if cellvalue==nValues[i]:
                        rows_string = rows_string + colors[i] + str(cellvalue) + delimiter_char
                        extreme_value = True
                        break
                if not extreme_value:
                    rows_string = rows_string + str(cellvalue) + delimiter_char
    rows_string = rows_string + '\\hline \n \\end{tabular}'
    if fulldocument:
        rows_string = rows_string + '}\n'
        rows_string = rows_string + '\n' +  r'\end{document}'
    return rows_string

def main():
    global smallest
    global nth
    global precision
    global fulldocument
    #Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("inputpath", help="the path to the .csv table")
    parser.add_argument("outputpath", help="the path where you want the .tex file")
    parser.add_argument("-s","--smallest", action="store_true",help="highlight smallest, default is largest")
    parser.add_argument("-p", "--precision", type=int, help="decimal precision, default is 3")
    parser.add_argument("-n", "--nelements", type=int, help="highlight largest/smallest, secondlargest/smallest, ..., nthlargest/smallest.\n Must be between 1 and 3")
    parser.add_argument("-f","--full", action="store_true",help="creates a complete .tex document, rather than only the tabular statement")
    args = parser.parse_args()
    if args.smallest:
        smallest = True
    if args.precision:
        precision = args.precision
    if args.nelements:
        if args.nelements > 3 or args.nelements < 1:
            print "nelements must be between 1 and 3!"
            sys.exit(2)
        nth = args.nelements
    if args.full:
        fulldocument = True

    #Read
    data_frame = pd.read_csv(args.inputpath,sep='\t')
    data_frame = data_frame.round(precision)

    #Get latex string
    result = get_latex_string(data_frame, nth)

    #Write result
    with open(args.outputpath, 'w') as out_file:
        out_file.write(result)

if __name__ == "__main__":
        main()
