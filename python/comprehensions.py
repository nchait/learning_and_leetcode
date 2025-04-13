from functools import reduce

dct = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "I": 9,
}

more_than_four = {k:v for k,v in dct.items() if v > 4}
print (more_than_four)
print (more_than_four.keys())
print ([n for n in more_than_four.keys()])
print (list(more_than_four.keys()))
print (more_than_four.values())

sum_a = reduce(lambda x, y:x+y, more_than_four.values())
print (sum_a)

print(sum(list(more_than_four.values())))

tdarr = [[1, 2, 3], [4, 5, 6], [2, 1, 2]]
print ("Sum = ",sum(map(sum,tdarr)))