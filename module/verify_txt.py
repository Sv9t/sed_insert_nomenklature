def verify(*args):
    """
    Стираем все что внутри pathLog и pathGet
    args[0]=pathLog, args[1]=pathGet
    """
    with open(args[0], 'w'):
        pass
    with open(args[1], 'w'):
        pass
