#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from sorts import (
    bogosort,
    # TODO: ImportError: No module named 'P26_InsertionSort'
    # bubble_sort,
    # bucket_sort,
    cocktail_shaker_sort,
    gnome_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    radix_sort,
    # TODO: remove this
    # random_normaldistribution_quicksort,
    selection_sort,
    shell_sort,
    topological_sort,
)


ALGO_LIST = {
    # 'bogosort': bogosort.bogosort,
    # 'bubble_sort': bubble_sort.bubble_sort,
    # 'bucket_sort': bucket_sort.bucketSort,
    "cocktail_shaker_sort": cocktail_shaker_sort.cocktail_shaker_sort,
    "gnome_sort": gnome_sort.gnome_sort,
    "heap_sort": heap_sort.heap_sort,
    "insertion_sort": insertion_sort.insertion_sort,
    "merge_sort": merge_sort.merge_sort,
    "quick_sort": quick_sort.quick_sort,
    "radix_sort": radix_sort.radixsort,
    # 'random_normaldistribution_quicksort': random_normaldistribution_quicksort.random_normaldistribution_quicksort,
    "selection_sort": selection_sort.selection_sort,
    "shell_sort": shell_sort.shell_sort,
    # 'topological_sort': topological_sort.topological_sort,
}
