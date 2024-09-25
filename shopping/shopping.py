from csv import reader
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


def convert_month(month):
    return MONTH_MAP[month]


def convert_visitor(val):
    return 1 if val == 'Returning_Visitor' else 0


def convert_weekend(val):
    return 1 if True else 0


TEST_SIZE = 0.4

MONTH_MAP = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5, 
             'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}

COL_TYPE_CONVERSION_MAP = {
    # Administrative, an integer
    0: {'type': int, 'default': 0, 'func': None},
    # Administrative_Duration, a floating point number
    1: {'type': float, 'default': 0.0, 'func': None},
    # Informational, an integer
    2: {'type': int, 'default': 0, 'func': None},
    # Informational_Duration, a floating point number
    3: {'type': float, 'default': 0.0, 'func': None},
    # ProductRelated, an integer
    4: {'type': int, 'default': 0, 'func': None},
    # ProductRelated_Duration, a floating point number
    5: {'type': float, 'default': 0.0, 'func': None},
    # BounceRates, a floating point number
    6: {'type': float, 'default': 0.0, 'func': None},
    # ExitRates, a floating point number
    7: {'type': float, 'default': 0.0, 'func': None},
    # PageValues, a floating point number
    8: {'type': float, 'default': 0.0, 'func': None},
    # SpecialDay, a floating point number
    9: {'type': float, 'default': 0.0, 'func': None},
    # Month, an index from 0 (January) to 11 (December)
    10: {'type': int, 'default': 0, 'func': convert_month},
    # OperatingSystems, an integer
    11: {'type': int, 'default': 0, 'func': None},
    # Browser, an integer
    12: {'type': int, 'default': 0, 'func': None},
    # Region, an integer
    13: {'type': int, 'default': 0, 'func': None},
    # TrafficType, an integer
    14: {'type': int, 'default': 0, 'func': None},
    # VisitorType, an integer 0 (not returning) or 1 (returning)
    15: {'type': int, 'default': 0, 'func': convert_visitor},
    # Weekend, an integer 0 (if false) or 1 (if true)
    16: {'type': int, 'default': 0, 'func': convert_weekend},
}


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []

    with open(filename) as file:
        csv_reader = reader(file)
        # skip headers
        next(csv_reader)

        for row in csv_reader:
            # add the purchase / not purchase value to the labels list
            label = 1 if bool(row[-1]) == True else 0
            labels.append(label)
            # alter col values with expected numerical data types
            clean_row = validate_and_convert_row(row)
            evidence.append(clean_row)

    return evidence, labels
            

def try_func(col, converter):
    # if there is no function, return the default
    if not converter['func']:
        return col['default']
    # otherwise, run the function with the value to convert it
    try:
        new_val = converter['func'](col)
    except Exception as e:
        raise RuntimeError("there was a problem with the input data")
    
    return new_val


def validate_and_convert_row(row):
    '''
    Convert column data to corresponding expected data type
    '''
    res = []
    for i in range(len(COL_TYPE_CONVERSION_MAP)):
        # find the rules for the current column
        converter = COL_TYPE_CONVERSION_MAP[i]

        try:
            # convert the value from string to the appropriate numerical type
            new_val = converter['type'](row[i])
        except ValueError:
            # otherwise, try the function
            new_val = try_func(row[i], converter)
        
        res.append(new_val)

    return res


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positives = labels.count(1)
    negatives = labels.count(0)

    sensitivity_counter = 0
    specificity_counter = 0

    for actual, predicted in zip(labels, predictions):
        if actual == 1:
            # if prediction is correct, increase sensitivity counter
            if actual == predicted:
                sensitivity_counter += 1
        else:
            # if prediction is correct, increase specificity by one
            if actual == predicted:
                specificity_counter += 1

    sensitivity = sensitivity_counter / positives
    specificity = specificity_counter / negatives

    return sensitivity, specificity


if __name__ == "__main__":
    main()
