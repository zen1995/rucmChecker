import argparse
from rucmLoader import RucmLoader
from rule import RuleLoader

if __name__== "__main__":
    '''
    parse args->load rule->load rucm -> foreach rule.check ->generate report
    '''
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser(description='RUCM文件检查工具')
    ap.add_argument("-r", "--rule", dest='rule_path', required=False, help="path to rule.json")
    ap.add_argument('rucm_path', nargs='?', default=None, type=str, help='path to whatYouNeedToCheck.rucm')
    
    args = ap.parse_args()

    print (args.rule_path)
    print (args.rucm_path)

    # load rule
    if args.rule_path:
        print ('Loading rule file: %s' % (args.rule_path))
        rule_load = RuleLoader(args.rule_path)
    else:
        print ('No rule file is specified. Default rules are loaded only.')

    # load rucm
    if args.rucm_path:
        print ('Checking rucm file: %s' % (args.rucm_path))
        rucm_loader = RucmLoader(args.rucm_path)
    else:
        print ('No rucm file is given. Check rule file only.')
    
