W = 25
H = 6

f = open("8.txt", "r")
image = f.readline()

layers = []

smallest = W*H*2
layer_id = 0
done = False
while(not done):
    layer_start = (W*H)*layer_id
    layer_end = layer_start + (W*H)

    if layer_end >= len(image):
        done = True
        break

    layer = image[layer_start:layer_end]
    layers.append(list(layer))

    count_0 = len(list(filter(lambda x:x=='0', layer)))
    count_1 = len(list(filter(lambda x:x=='1', layer)))
    count_2 = len(list(filter(lambda x:x=='2', layer)))

    if count_0 < smallest:
        smallest = count_0
        smallest_result = count_1 * count_2

    layer_id = layer_id + 1

print("number of layers:", layer_id)

out_layer = [2]*W*H
for p in range(0, W*H):
    for l in layers:
        if l[p] != '2':
            out_layer[p] = l[p]
            break

# display layer
for y in range(0, H):
    for x in range(0, W):
        p = out_layer[y*W + x]
        if p == '1':
            print("X", end='')
        else:
            print(" ", end='')
    print()
