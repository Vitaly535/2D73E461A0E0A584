import datetime
import io
import math
import re
import time

import matplotlib.pyplot as plt


def getX(interval, dt):
    """ Создает список значений аргументов"""
    timenow = int(time.time())
    timestep = dt * 3600
    timeinterval = interval * 3600 * 24
    timerange = int((interval * 24 / dt) + 1)
    arr = [str(timenow - timeinterval + timestep * z)
           for z in range(timerange)]
    arr1 = [datetime.datetime.fromtimestamp(
        timenow - timeinterval + timestep * z).strftime('%Y-%m-%d %H:%M:%S')
        for z in range(timerange)]
    return arr, arr1


def getY(arrx, func):
    """ Создает список значений функции"""
    arry = []
    for item in arrx:
        y = getrepl(func, item)
        if y[1]:
            arry.append(y[0])
        else:
            print(y[0])
            return y[0], False
    return arry, True


ALLOWED_NAMES = {
    k: v for k, v in math.__dict__.items() if not k.startswith("__")
}


def getrepl(func, rpl='1'):
    """ Подставляет значение t в выражение и выполняет его"""
    expression = re.sub("(?<=[^a-zA-Z_.])t(?=[^a-zA-Z_.])",
                        rpl, ' ' + func + ' ')
    try:
        result = evaluate(expression.replace(' ', ''))
        return result
    except SyntaxError:
        return("Некорректное выражение.", False)
    except (NameError, ValueError) as err:
        return err, False
    except Exception as err:
        return (err, False)


def evaluate(expression):
    """Вычисляет математическое выражение."""
    code = compile(expression, "<string>", "eval")
    for name in code.co_names:
        if name not in ALLOWED_NAMES:
            return f"Неизвестный оператор '{name}'", False
    return eval(code, {"__builtins__": {}}, ALLOWED_NAMES), True


def plott(arr1, arr2):
    """ Рисует график"""
    plt.clf()
    plt.plot(arr1, arr2, label='функция')
    ax = plt.gca()
    ax.grid(True)
    ln = int(len(arr1) / 10)
    plt.xticks(rotation=90)
    i = 0
    for label in ax.get_xaxis().get_ticklabels():
        if i % ln > 0:
            label.set_visible(False)
        i += 1
    plt.xlabel('time interval')
    plt.ylabel('function result ')
    plt.title("Function Plot")
    plt.legend()
    f = io.BytesIO()
    plt.savefig(f, bbox_inches="tight")
    plt.clf()
    print('done')
    return f
