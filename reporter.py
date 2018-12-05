import sys
import typing


class ErrorInfo:
    def __init__(self, rulename, usecasename, sentence):
        self.rulename: str = rulename
        self.usecasename: str = usecasename
        self.sentence: str = sentence


class Reporter():
    errors: typing.List[ErrorInfo] = []
    reporter = sys.stdout

    @staticmethod
    def generateReport(filePath: str)->None:
        Reporter.reporter = open(filePath, "w", encoding="utf-8")

    @staticmethod
    def reportError(rulename='', usecasename='', sentence=''):
        Reporter.errors.append(ErrorInfo(rulename, usecasename, sentence))

    @staticmethod
    def report(destination=reporter):
        for e in Reporter.errors:
            destination.write(
                f"Sentence ({e.sentence}) in use case({e.usecasename}) violates the rule({e.rulename}).\n")


if __name__ == "__main__":
    print('-' * 20, 'test Report', '-' * 20)
    # Reporter.generateReport('report.txt')
    Reporter.reportError('rule1', 'usecase1', 'I am kind')
    Reporter.reportError('rule2', 'usecase2', 'I am dog')
    Reporter.reportError('rule3', 'usecase3', 'I am cat')
    Reporter.reportError('rule4', 'usecase4', 'I am monkey')
    for e in Reporter.errors:
        Reporter.reporter.write(
            f"Sentence ({e.sentence}) in use case({e.usecasename}) violates the rule({e.rulename}).\n")
    print('-' * 60)
