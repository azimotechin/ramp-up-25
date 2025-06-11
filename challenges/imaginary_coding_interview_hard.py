def interview(lst, tot):
    if len(lst) != 8:
        return "disqualified"
    if lst[0] > 5 or lst[1] > 5:
        return "disqualified"
    if lst[2] > 10 or lst[3] > 10:
        return "disqualified"
    if lst[4] > 15 or lst[5] > 15:
        return "disqualified"
    if lst[6] > 20 or lst[7] > 20:
        return "disqualified"
    if tot > 120:
        return "disqualified"
    return "qualified"