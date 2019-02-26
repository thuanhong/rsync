list = [6,3,5,7,2,1,9,8,4]

def sort(list, l, r):
    if l > r: return
    pivot = list[int(((l + r) / 2))]
    i = l
    j = r
    while (i <= j):
        while (list[i] < pivot):
            i += 1
        while (list[j] > pivot):
            j -= 1
        if i <= j:
            list[i], list[j] = list[j], list[i]
            i += 1
            j -= 1

    sort(list, l, j)
    sort(list, i, r)

print(sort(list, 0, len(list) - 1))
