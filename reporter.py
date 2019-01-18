import sys
import typing
import jinja2
# https://wkhtmltopdf.org/downloads.html
import pdfkit


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

    @staticmethod
    def to_html(destination_file):
        loader = jinja2.FileSystemLoader('./base.html')
        env = jinja2.Environment(loader=loader)
        template = env.get_template('')

        items = []
        for e in Reporter.errors:
            items.append({
                'description': e.rulename,
                'usecasename': e.usecasename,
                'sentence': e.sentence
            })

        result = template.render(items=items)

        with open(destination_file, "w") as text_file:
            print(result, file=text_file)

        return result

    @staticmethod
    def to_pdf(destination_file):
        Reporter.to_html('temp.html')
        pdfkit.from_file('temp.html', destination_file) 


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
    print(Reporter.to_html('sdf.html'))
    Reporter.to_pdf('sdf.pdf')
