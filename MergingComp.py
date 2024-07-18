import json

def main():
    ee = json_read('ee.json') #Adjacency matrix represented as 2d list
    ew = json_read('ew.json') #Adjacency matrix represented as 2d list

    ee_intersect_ew = matrix_intersection(ee, ew)
    ee_comp_ew = matrix_composition(ee, ew)
    ew_comp_ee = matrix_composition(ew, ee)
    merged_data = matrix_union(ee, ew)
    data_2_hop = matrix_mult(merged_data, merged_data)
    two_or_less = matrix_union(data_2_hop, merged_data)
    data_3_hop = matrix_mult(data_2_hop, merged_data)
    three_or_less = matrix_union(data_3_hop, two_or_less)
    data_4_hop = matrix_mult(data_3_hop, merged_data)
    four_or_less = matrix_union(data_4_hop, three_or_less)
    reachable = final_order_matrix(merged_data)
    json_write('ee1ew1', ee_comp_ew)
    json_write('ew1ee1', ew_comp_ee)
    json_write('nutsRedundancies', ee_intersect_ew)
    json_write('nuts1', merged_data)
    json_write('nuts2', data_2_hop)
    json_write('nuts2orLess', two_or_less)
    json_write('nuts3', data_3_hop)
    json_write('nuts3orLess', three_or_less)
    json_write('nuts4', data_4_hop)
    json_write('nuts4orLess', four_or_less)
    json_write('nutsT', reachable)







def get_tuples(lyst):
    ret = []
    for r_i, row in enumerate(lyst):
        for c_i, col in enumerate(row):
            if col == 1:
                ret += (r_i, c_i),
    return ret

def matrix_mult(mat_a, mat_b):
    matrix = [[min(sum(a*b for a,b in zip(X_row,Y_col)),1) for Y_col in zip(*mat_b)] for X_row in mat_a]
    for row in matrix:
        for col in row:
            col = min(col, 1)
    return matrix

def final_order_matrix(mat):
    length = len(mat)
    cur = mat
    for i in range(length):
        new_matrix = matrix_mult(cur, mat)
        cur = matrix_union(new_matrix, cur)

    return cur


def matrix_composition(mat_a, mat_b):
    matrix_tup = []

    for r_i, row in enumerate(mat_a):
        for c_i, col in enumerate(row):
            if col == 1:
                for col_i_b, col_b in enumerate(mat_b[c_i]):
                    if col_b == 1:
                        matrix_tup += (r_i, col_i_b),

    matrix = [[0 for i in range(len(mat_a))] for i in range(len(mat_b))]
    for x, y in matrix_tup:
        matrix[x][y] = 1

    return matrix

def matrix_intersection(mat_a, mat_b):
    a_tup = get_tuples(mat_a)
    b_tup = get_tuples(mat_b)
    common_tup = []

    for x, y in a_tup:
        if (x, y) in b_tup:
            common_tup += (x, y),

    matrix = [[0 for i in range(len(mat_a))] for i in range(len(mat_b))]
    for x, y in common_tup:
        matrix[x][y] = 1

    return matrix

def matrix_union(mat_a, mat_b):
    a_tup = get_tuples(mat_a)
    b_tup = get_tuples(mat_b)
    union_tup = a_tup + b_tup

    matrix = [[0 for i in range(len(mat_a))] for i in range(len(mat_b))]
    for x, y in union_tup:
        matrix[x][y] = 1

    return matrix


def json_read(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def json_write(file_path, data):
    with open(file_path + '.json', 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    main()
