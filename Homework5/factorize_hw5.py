from multiprocessing import Pool
import time


def factorize(number):
    i = 1
    results = []
    while i <= number:
        if number % i == 0:
            results.append(i)
        i += 1
    return results


def main():
    numbers = [128, 255, 99999, 10651060]
    with Pool(processes=2) as pool:
        results = pool.map(factorize, numbers)
    a, b, c, d = results

    # a = factorize(128)
    # b = factorize(255)
    # c = factorize(99999)
    # d = factorize(10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553,
                 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    print(end)