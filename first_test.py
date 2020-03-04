
from math import ceil, floor

m1 = 2 ** 3

studentList = ['Mike', 'Author', 'Peter', 'Tony']

companyList = ['Apple', 'Google', 'Facebook', 'Microsoft', 'Sony', 'Toshiba', 'Nissan']


bookPriceDict = {
    'No Way': 90,
    'Faraway From My Farm': 100,
    'Three Kingdoms': 10
}

numberList = ['101', '33', '44', '19']
mixList = [999, 'Mike', 'Nike', 'Ada']

maxSimFloat = float('190.999')
# print(round(maxSimFloat))
# print('floor float number = ' + str(floor(maxSimFloat)))
# print('ceil float number = ' + str(ceil(maxSimFloat)))

# numberList[10] = '299'
# for num in numberList:
#     print(num)

index = 0
while index < companyList.__len__():
    # print(companyList[index])
    index += 1
    # print('index = ' + index)

# print('Hello "Motion"!')
# print("Hi 'Local'!")

# bookNames = bookPriceDict.keys()
# for b in bookNames:
#     print(b + ':' + str(bookPriceDict[b]))


count = 100


def change_count(c):
    c += 1
    strings = ','.join(studentList)
    print(strings)


MY_NAME = 'ZHENGWEIBIN'


def info_my_name():
    z_index = MY_NAME.index('Z')
    find_i = MY_NAME.find('I')
    print('z index = ', z_index)
    print('find i = ', find_i)
    print('find Mike in student list , ', studentList.index('Tony'))


# change_count(count)
info_my_name()
# print('count = ' + str(count))
