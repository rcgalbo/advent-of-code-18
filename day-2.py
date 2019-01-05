'''
advent of code day 2: Inventory managment system

part one 

ID containing exactly two of any letter
separately counting those with exactly three of any letter

function to count unique letter

'bababc' contains two a and three b, so it counts for both.
'abbcde' contains two b, but no letter appears exactly three times.
'abcccd' contains three c, but no letter appears exactly two times.
'aabcdd' contains two a and two d, but it only counts once.
'abcdee' contains two e.
'ababab' contains three a and three b, but it only counts once.

part two

find correct ids that differ by one character   

'kabcde'
'fghij'
'klmno'
'pqrst'
'fguij'
'axcye'
'wvxyz'
'''
from collections import Counter

# part two
def count(str):
    return Counter(str)

assert count('bababc') == {'b':3, 'a':2, 'c':1}

def exactly_two(collection):
    if 2 in collection.values():
        return 1
    return 0

assert exactly_two(count('bababc')) == 1

def exactly_three(collection):
    if 3 in collection.values():
        return 1
    return 0

assert exactly_three(count('bababc')) == 1

# part two
def distance(str1, str2):
    dist = 0
    for i,j in zip(str1,str2):
        if i!=j: dist+=1
    return dist

assert distance('abcde', 'axcye') == 2
assert distance('fghij','fguij') == 1

def common_letters(str1, str2):
    common = []
    for i,j in zip(str1,str2):
        if i==j: common.append(j)
    return common

if __name__ == '__main__':
    data = [ 
    'evsialkqydurohxqpwbcugtjmh',
    'evsialkqydurohxzssbcngtjmv',
    'fvlialkqydurohxzpwbcngujmf',
    'nvsialkqydorohxzpwpcngtjmf',
    'evsialjqydnrohxypwbcngtjmf',
    'vvsialyqxdurohxzpwbcngtjmf',
    'yvsialksydurowxzpwbcngtjmf',
    'evsillkqydurbhxzpmbcngtjmf',
    'ivsialkqyxurshxzpwbcngtjmf',
    'ejsiagkqyduhohxzpwbcngtjmf',
    'evsialkqldurohxzpcbcngtjmi',
    'evsialkqydurohxzpsbyngtkmf',
    'ersialkeydurohxzpwbcngtpmf',
    'evsialuqzdkrohxzpwbcngtjmf',
    'evswulkpydurohxzpwbcngtjmf',
    'evsialkqyiurohxzpwucngttmf',
    'evtialkqydurphxzywbcngtjmf',
    'evsialkzyiurohxzpwbcxgtjmf',
    'evsiaykqydurohxzpwbcggtjuf',
    'evxqalkqydurohmzpwbcngtjmf',
    'eisralkqydurohxzpdbcngtjmf',
    'evsfalkqydurohxzpwbangtjwf',
    'evbialkqydurohxzawbcngtjmg',
    'evsialkqydrrohxrpcbcngtjmf',
    'evsialkqycurohxzpvbcngtjkf',
    'evsialkqsdudohxzpwbcnotjmf',
    'evsiackqydurohxzpmbsngtjmf',
    'evsialmqykurohxzpwbfngtjmf',
    'evsialsqydurohxzpwucngtjxf',
    'tvsialkqyeurohxzpwbcrgtjmf',
    'zvsialkqydbrohxzpwbcnltjmf',
    'evsmbskqydurohxzpwbcngtjmf',
    'evsialkqydurohxzpwbcngpgmt',
    'evsialkqydurlyezpwbcngtjmf',
    'evoialkqyturohxzpwbcnjtjmf',
    'evsialkqydurohxspkfcngtjmf',
    'evsiaikqydurohxjpwbcngtjmd',
    'evsialkyydurohxzvwbcngtjmc',
    'svsialkqyduhohxzpwbhngtjmf',
    'eysillkqydurohxzhwbcngtjmf',
    'evsialkqyduetaxzpwbcngtjmf',
    'evsialkqxdurshxzpwbcngtjmb',
    'evsiadkqydwrovxzpwbcngtjmf',
    'evsialkqydurokxzpwbcngjjef',
    'evskalkqymurohxzpybcngtjmf',
    'cvsialkqydurohxzpwbcnbtjma',
    'evsialkqydurohxzawhcngtjuf',
    'evsiahkqfduroixzpwbcngtjmf',
    'evsivlkqyduroqxzpwbctgtjmf',
    'evsiarkqyduroixzywbcngtjmf',
    'evspalkqydurohxzpwlcngxjmf',
    'eesialkqydurohxzpalcngtjmf',
    'gvsualkqydurohxzpwbmngtjmf',
    'evsialkqydurlhxzpwbcngsjmq',
    'evsialhqydfrohxopwbcngtjmf',
    'evzialkqydsrohxzpwbcngtjmw',
    'evbpalkqydurbhxzpwbcngtjmf',
    'mvsialkqydurohxzpwbcnghjmr',
    'evsialkqsdurohxzpkbcngtjxf',
    'ejkialktydurohxzpwbcngtjmf',
    'evsialkqyauoohxzpwbqngtjmf',
    'evsiklkyyduroqxzpwbcngtjmf',
    'evgialkqydurohxzpwocngthmf',
    'ebsialkqydcrohxzpwbcngtbmf',
    'evsialkqysurohxzpwfingtjmf',
    'evsialkqddurmhxzpwbnngtjmf',
    'evsialkqydurohxoiwwcngtjmf',
    'evsialkqydurohpzkzbcngtjmf',
    'vvsealkqydurorxzpwbcngtjmf',
    'evsialkqyduroqxzpwlungtjmf',
    'eviialkqiyurohxzpwbcngtjmf',
    'evzsalkqyaurohxzpwbcngtjmf',
    'exsialkqydurohfzpwbwngtjmf',
    'evsialkqyduruhxkpwbcnytjmf',
    'essiatkqydurohxzpwbxngtjmf',
    'evsialkqyduroamzpwbcngtjcf',
    'wvsialkqyduruhxzpwbcnxtjmf',
    'evsialkqydurohxgpwbcngtjeh',
    'evsialfqxdurohxzpwbcngtomf',
    'evsialkqyourghxzpwbcngtbmf',
    'evsoaokqydurohxzpwbcngtamf',
    'evsialpqydurohxzpwccxgtjmf',
    'evsialkqzdurxhxgpwbcngtjmf',
    'ezsialkqmdurohxzpwbcngtjmi',
    'cvsialjeydurohxzpwbcngtjmf',
    'evsialkqydurocxupwbcvgtjmf',
    'evscalkqydtrohxzpebcngtjmf',
    'evjialkqyduiohxzpabcngtjmf',
    'evsialjqyduruhxzppbcngtjmf',
    'evsialkqydurfhxzpwbcuqtjmf',
    'evsialkqyiurohizpwucngttmf',
    'evsialiqydurrhxzpwbcngdjmf',
    'evbialkqywurohxzpwhcngtjmf',
    'evsialkqyduloyxzpwbqngtjmf',
    'evsialxqyduzohxzpwbqngtjmf',
    'vvsialkqydurohxzpwbcnqpjmf',
    'evsialksydurohxzcwbmngtjmf',
    'pvsialkqydurohxzpwucngtjvf',
    'evsialkqydurohmkpwbcngtfmf',
    'mvsialkqydurphyzpwbcngtjmf',
    'evsialkqydyrohxzhwbcnitjmf',
    'evsialokydurozxzpwbcngtjmf',
    'evsialkqyduroexfcwbcngtjmf',
    'evsiavkqydurohxzpwbcnmtjme',
    'evsiawkqydurohxzpwbcngojjf',
    'evsialkaydurohxzpwfcngtjff',
    'evsialkaydurohxzpwbcngtjpb',
    'gvsialkqyburorxzpwbcngtjmf',
    'evszalkqydurphxzpwocngtjmf',
    'evsualkqyduropxzpwbcngejmf',
    'evsitlkqydurshxzpwbcngtkmf',
    'evbixlkqydrrohxzpwbcngtjmf',
    'elsialkqydprohxzpwbcngtrmf',
    'evsialkqydurohbzpwbcggtjmc',
    'evtoalqqydurohxzpwbcngtjmf',
    'evsralhqydurohxzowbcngtjmf',
    'evsialkhydurohxzlsbcngtjmf',
    'evsialkqydurohxvpwbcnuujmf',
    'evsialkqydurocxzuwbcngtjmi',
    'evsialkqndyrokxzpwbcngtjmf',
    'evsialkqydurywfzpwbcngtjmf',
    'evsialkqydurohxzwwbcngthms',
    'eqsiahkqydurohxzpwbyngtjmf',
    'evsdalkqydurohxzpwbcnjkjmf',
    'evsialkqyddrohplpwbcngtjmf',
    'evshalkqydurohxzpfxcngtjmf',
    'evvialkqydurohxapwbcngtjmh',
    'evsialkqyduvohxzpwbcnnvjmf',
    'evsiblkqedurohxzpwbkngtjmf',
    'evsvalkqfdutohxzpwbcngtjmf',
    'evsialjqydurohxzpwbcnctjsf',
    'evsialkxywurohxdpwbcngtjmf',
    'evsiagkqydurohxzpwzcjgtjmf',
    'ebsialkqydurohxzpxfcngtjmf',
    'evsialkqysfrohxzpwbcngtjlf',
    'evvialkqyqurwhxzpwbcngtjmf',
    'evxialkqydurohxzpwgcnrtjmf',
    'vvsillkqydurohxzpwbcvgtjmf',
    'evsiwlkqyduoohxzpwbcngtjxf',
    'evsialkqypurohezpwbcngtjwf',
    'evbialkqydurohxipwbcnftjmf',
    'evsiakkqyduyohxzpwbcngtjmu',
    'evsialkqydurohzzpwxqngtjmf',
    'evsialkqykurkhxzpwocngtjmf',
    'dvriplkqydurohxzpwbcngtjmf',
    'evsialkqgdurohxzpwbmnctjmf',
    'evsialkqyuurohxzpwtcngtjmj',
    'wvsialkqydurohxzpwbchgejmf',
    'eusimlsqydurohxzpwbcngtjmf',
    'evsialkqydqrohxzhwbcngtjmh',
    'wvswalkqydurohxzpwbcngjjmf',
    'evsialkqyourohxzkwbcngttmf',
    'evaialkqydurohxzbubcngtjmf',
    'evfialkqydueohxzpwbclgtjmf',
    'evrialkqydurohxzpwbcnctjmh',
    'evsiaojqydxrohxzpwbcngtjmf',
    'evsualkqywuxohxzpwbcngtjmf',
    'evsialkdydrzohxzpwbcngtjmf',
    'evlialkqyfurohxzpwbcnotjmf',
    'epsialkqydujohxzpwbcngtjif',
    'evsialkqyaucohxgpwbcngtjmf',
    'lvsialaqydurohxzpwbcngtjzf',
    'evsialkgydurohezpwbcngtjmo',
    'lvsialkqydurosxwpwbcngtjmf',
    'evsiaekqyqurohxzpvbcngtjmf',
    'evsiapkqydirohxzpwbzngtjmf',
    'zvsixlkwydurohxzpwbcngtjmf',
    'evaialkqyduoohxzpwbcngtjkf',
    'evsialcqedurohxzpwbcngtjmc',
    'evjialkgydurohxzpwbwngtjmf',
    'evsialkqcdurohxzpwbcpgojmf',
    'evsialkqkdurohxzlwbcngtrmf',
    'eosiylkzydurohxzpwbcngtjmf',
    'evsialkqydurohhzpwscnmtjmf',
    'evsiallqydurobxzpwbxngtjmf',
    'evsialkqydurohwztwhcngtjmf',
    'evsiallqydurohxzpwbcygjjmf',
    'evsiabkqywurohxzpwbcngtjmy',
    'evsiackqydzrohxznwbcngtjmf',
    'evsiazkqzdurooxzpwbcngtjmf',
    'evsialcqydurghxzpwbcngtjmc',
    'yvsiaxkqydurohxzpwbcxgtjmf',
    'evsiylkqgdhrohxzpwbcngtjmf',
    'lvsialkqydurohxgcwbcngtjmf',
    'evsiglkqydurohxzpwbvngzjmf',
    'evsialkqyvurohxzpwbcngtjnz',
    'evsialkgydueohxzpwbcpgtjmf',
    'cvsiavkqyddrohxzpwbcngtjmf',
    'evsialklyrurohxzpwbcngtjff',
    'eisialkqyduwohxzpwbcngcjmf',
    'evsialkqydrrihwzpwbcngtjmf',
    'easialkqydurohxzpwbcnltrmf',
    'evsialfqydurohxzpybcnytjmf',
    'eqsialkqycurohxzywbcngtjmf',
    'evsitlkqmdurohxzpwbcngtjmx',
    'evsiclsqyduroixzpwbcngtjmf',
    'elsialrqydurohxzpwmcngtjmf',
    'evsiapkqodurohxzpwbcogtjmf',
    'evstalkeydurohxzpibcngtjmf',
    'evsihlkqyqurohxzpwblngtjmf',
    'euszalkqydurohxipwbcngtjmf',
    'ezsialksydurohxzpwbcngfjmf',
    'eisialkdydurohxzpwbcngtumf',
    'evsirlkaydprohxzpwbcngtjmf',
    'evsiklkqydnrohxzpwbcngtjmu',
    'evsialkqydnuohxzpwbcngtjmu',
    'eksialkqydurohxztwfcngtjmf',
    'evlialkqedurohxzpwbhngtjmf',
    'evqialkqydurohxzpubcngtjpf',
    'evsialkwydurohwzpwbcnmtjmf',
    'evsiaokqcdurohxzpwbcngtjcf',
    'evsialkkyfurohxzpvbcngtjmf',
    'evsialkqyduromxzpwqcngtimf',
    'evsialkqydumohxzpwbcnmtjsf',
    'evsialddydurehxzpwbcngtjmf',
    'evsialkqydurohxzpobcnptjmk',
    'evsiagkqydurohhzpwbcxgtjmf',
    'evsfalkqydurohszpwbangtjmf',
    'evgialkzyduqohxzpwbcngtjmf',
    'evaialkqzdurohxzpwbcngtjmo',
    'evsialkqyqurohxjpwbcnntjmf',
    'evsialkjydybohxzpwbcngtjmf',
    'evskalgqydurohxzrwbcngtjmf',
    'evsialkqydurohxzpjbcymtjmf',
    'evsialkqqdurohxzpybcngtjyf',
    'evsialkqydqrbhxzpwbcngtjmj',
    'evssalaqrdurohxzpwbcngtjmf',
    'mvsialkfydurohxzpwbcngtjmk',
    'evsialkqwdurohxzpwgcngtjdf',
    'evqkalkqydurohxzpwbcngajmf',
    'evbialkqydurohxzpibcngejmf',
    'evszalkqydurbhxzpwbcngtjsf',
    'evsialkqydurohxepwbcngtjjo',
    'evsialkqcdubmhxzpwbcngtjmf',
    'evsiarkqyduroaxzpwbcngtjmp',
    'evsiakkqyduzohczpwbcngtjmf',
    'evtualkqydurofxzpwbcngtjmf',
    'ejsialkqvdurohzzpwbcngtjmf',
    'evsialkqydurohczpwbcngqvmf',
    'svsianfqydurohxzpwbcngtjmf',
    'evsialiqydurohxzpwbcngzqmf',
    'ejsialhqydurohxzpwjcngtjmf',
    'evpialkqydurohxzpwbcnbtjff',
    'evsialkuyvurohxzpwbcngtjkf',
    'eqsialkqydurohxzpwbcnwtcmf',
    'evsiatkqydkrohxzpwkcngtjmf',
    'evsialkqydurohxzpebciytjmf',
    'evsialkqydrrohxzpwtcngtfmf',
    'evsialkqjducohxzpwycngtjmf',
    'evsialkqydurohxzpwicnxtjnf'
    ]

    c = (list(map(count,data)))

    two = sum(list(map(exactly_two, c)))
    three = sum(list(map(exactly_three, c)))

    # print(two * three)

    common = []
    for i in data[:-2]:
        for j in data[1:]:
          if distance(i,j) == 1:
              common.append(common_letters(i,j))
    print([''.join(c) for c in common])