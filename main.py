import argparse
from rucmLoader import RucmLoader
from reporter import Reporter
from RuleLoader import RuleLoader
import rule
import json
import nlputils

if __name__ == "__main__":
    '''
    $ python3 main.py --rule=rule-template.txt --url=localhost:9000 test1.rucm
    parse args->load rule->load rucm -> foreach rule.check ->generate report
    '''
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser(description='RUCM文件检查工具')
    ap.add_argument("-r", "--rule", dest='rule_path',
                    required=False, help="path to rule.json")
    ap.add_argument("-u", "--url", dest='nlp_server', default='http://10.133.6.180:9000/',
                    required=False, help="url to nlp server")
    ap.add_argument('rucm_path', nargs='?', default=None,
                    type=str, help='path to whatYouNeedToCheck.rucm')

    args = ap.parse_args()

    # print(args.rule_path)
    # print(args.rucm_path)
    # print(args.nlp_server)

    if args.nlp_server:
        nlputils.url = args.nlp_server

    # load rule
    if args.rule_path:
        print('Loading rule file: %s' % (args.rule_path))
        try:
            rule_load = RuleLoader(args.rule_path)
            # print(f'Load successfully! Result: \n{rule_load}')
        except (FileNotFoundError, json.JSONDecodeError) as err:
            print(err)
    else:
        print('No rule file is specified. Default rules are loaded only.')

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

    Reporter.report()
