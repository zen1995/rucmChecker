import argparse
from rucmLoader import RucmLoader
from reporter import Reporter
from RuleLoader import RuleLoader
import rule
import json
import nlputils

if __name__ == "__main__":
    '''
    $ python3 main.py --rule=rule-template.txt --url_en=http://localhost:9000 --url_han=http://localhost:9001 test/test_1.rucm
    parse args->load rule->load rucm -> foreach rule.check ->generate report
    '''
    # construct the argument parse and 
    #  the arguments
    ap = argparse.ArgumentParser(description='RUCM文件检查工具')
    ap.add_argument("-r", "--rule", dest='rule_path',default="./rule-template.txt",
                    required=False, help="path to rule.json")
    ap.add_argument("-u", "--url_en", dest='nlp_server', default=nlputils.url_En,
                    required=False, help="url to nlp server")
    ap.add_argument("-uh", "--url_han", dest='nlp_han_server', default=nlputils.url_Han,
                    required=False, help="url to nlp chinese server")
    ap.add_argument('rucm_path', nargs='?', default=None,
                    type=str, help='path to whatYouNeedToCheck.rucm')

    args = ap.parse_args()

    # print(args.rule_path)
    # print(args.rucm_path)
    # print(args.nlp_server)

    if args.nlp_server:
        nlputils.url_En = args.nlp_server
    if args.nlp_han_server:
        nlputils.url_Han = args.nlp_han_server

    rule_load = None
    # load rule
    if args.rule_path:
        print('Loading rule file: %s' % (args.rule_path))
        try:
            rule_load = RuleLoader(args.rule_path)
            rule_load.load()
            print(f'Load successfully! Result: \n{rule_load}')
        except (FileNotFoundError, json.JSONDecodeError) as err:
            print(err)
    else:
        print('No rule file is specified. Default rules are loaded only.')

    rucm_loader = None
    # load rucm
    if args.rucm_path:
        print('Checking rucm file: %s' % (args.rucm_path))
        rucm_loader = RucmLoader(args.rucm_path)
        print(f'Load successfully! Result: \n{rucm_loader}')
    else:
        print('No rucm file is given. Check rule file only.')

    # print(rule_load)

    print('---'*65)
    if rucm_loader and rule_load:
        print('--------------check processing-------------')
        print(rule.RuleDB.userRules)
        print(rule.RuleDB.defaultRules)
        for i in rule.RuleDB.userRules:
            print('---', i.check)
            i.check()
        for i in rule.RuleDB.defaultRules:
            print('---', i.check)
            i.check()

    print('-' * 20, 'report', '-' * 20)
    Reporter.report()
    Reporter.to_pdf('result.pdf')
