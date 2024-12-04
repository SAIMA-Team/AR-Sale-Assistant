required_words = ["item", "component", "product"]

num = 4
# At least one of these words should be present
availability_words = ["have", "available", "item"]

required_present = any(word in required_words for word in availability_words )

if required_present:
    print(f"we have {num}")


def condition(num1, num2):
    if num1 == num2:
        print(f"num1 is equal to num2")
    elif num1 > num2:
        print(f"num1 is larger than num2")
    else:
        print(f"num2 is larger than num1")

condition(4,5)

def condition(num1, num2):
    if num1 == num2:
        return (f"num1 is equal to num2")
    elif num1 > num2:
        return (f"num1 is larger than num2")
    else:
        return (f"num2 is larger than num1")

result = condition(4,5)


def cal(num1, num2, choice):
    if choice == 1:
        return num1 + num2
    elif choice == 2:
        return num1 - num2
    elif choice == 3:
        return num1 * num2
    elif choice == 4:
        if num2 == 0:
            return f"can not divide by zero"
        else:
            return num1 + num2
    else:
        return f"please enter a valid operator"
    
result = cal(7,3,4)
print(result)


i = 0

count = 0

list = [4,2,6,7,9,1]

while i < len(list):
    count += list[i]
    i+=1

print(count)

j = 0
k = 0
        
list1 = [2,5,8,3,0,6]
list2 = [4,5,9,3,6,4]

for i in range(len(list1)):
    for j in range(len(list2)):
        print(f"values are: {list1[i] + list2[j]}")
        j+=1
    i+=1
print(f"complete")

