__author__ = "ipetrash"

## Example of using pipe module

# https://github.com/JulienPalard/Pipe
# ru: http://habrahabr.ru/post/117679/
import pipe


if __name__ == "__main__":
    print((i for i in range(10)) | pipe.as_list)  # tuple to list
    print([i for i in range(10)] | pipe.as_tuple)  # list to tuple
    print(((1, 1), ("a", 2), (3, "d")) | pipe.as_dict)  # tuple to dict

    print()
    # list of even numbers
    l = (i for i in range(10)) | pipe.where(lambda x: x % 2 is 0) | pipe.as_list
    c = l | pipe.count  # count elements
    print("List: {}, count: {}".format(l, c))
    print()

    # custom pipe:
    @pipe.Pipe
    def custom_add(x):
        return sum(x)

    print([1, 2, 3, 4] | custom_add)  # = 10
