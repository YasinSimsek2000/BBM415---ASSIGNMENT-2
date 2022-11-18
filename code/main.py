import numpy as np
from PIL import Image
import numpy


def get_ssd(array1, array2):
    ssd = 0
    for x in range(0, array1.shape[0]):
        ssd += numpy.sum(numpy.square(numpy.subtract(array1[x], array2[x])))
    return ssd


def get_mean(x_limit_s, x_limit_f, y_limit_s, y_limit_f, array):
    return numpy.mean(array[x_limit_s:x_limit_f, y_limit_s:y_limit_f, 0]), \
           numpy.mean(array[x_limit_s:x_limit_f, y_limit_s:y_limit_f, 1]), \
           numpy.mean(array[x_limit_s:x_limit_f, y_limit_s:y_limit_f, 2])


def get_std(x_limit_s, x_limit_f, y_limit_s, y_limit_f, array):
    return numpy.std(array[x_limit_s:x_limit_f, y_limit_s:y_limit_f, 0]), \
           numpy.std(array[x_limit_s:x_limit_f, y_limit_s:y_limit_f, 1]), \
           numpy.std(array[x_limit_s:x_limit_f, y_limit_s:y_limit_f, 2])


def color_transfer(source_image_panel, x_start, x_finish, y_start, y_finish,
                   source_mean, target_mean, source_std, target_std):
    for x in range(x_start, x_finish):
        for y in range(y_start, y_finish):
            old_pixel = source_image_panel[x][y]
            new_pixel = (old_pixel - source_mean) * (target_std / source_std)
            new_pixel += target_mean
            new_pixel = round(new_pixel)

            if new_pixel > 255:
                new_pixel = 255
            elif new_pixel < 0:
                new_pixel = 0

            source_image_panel[x][y] = new_pixel

    return source_image_panel


def color_transfer_according_to_ssd(source_image_array, target_image_array):
    y = target_image_array.shape[1] // 2
    if target_image_array.shape[0] > source_image_array.shape[0]:
        x = source_image_array.shape[0]
    else:
        x = target_image_array.shape[0]

    x = x // 2

    source_image_array = [source_image_array[m:m + x, n:n + y] for m in range(0, target_image_array.shape[0], x)
                          for n in range(0, y * 2, y)][:4]

    target_image_array = [target_image_array[m:m + x, n:n + y] for m in range(0, target_image_array.shape[0], x)
                          for n in range(0, y * 2, y)][:4]

    limits_of_regions = []

    for m in range(0, 4):
        best_ssd = float("inf")
        matching = (0, 0)
        for n in range(0, 4):
            current_ssd = get_ssd(source_image_array[m], target_image_array[n])
            if current_ssd < best_ssd:
                best_ssd = current_ssd
                matching = (m, n)
        l_source = matching[0] // 2 * x, matching[0] // 2 * x + x, (matching[0] % 2) * y, (matching[0] % 2) * y + y
        l_target = matching[1] // 2 * x, matching[1] // 2 * x + x, (matching[1] % 2) * y, (matching[1] % 2) * y + y
        limits_of_regions.append((l_source, l_target))

    return limits_of_regions


image_sources = []
image_targets = []
sources = []
targets = []

for i in range(1, 16):
    s_image = Image.open("photos/source{}.png".format(i))
    t_image = Image.open("photos/target{}.png".format(i))
    source_image = numpy.array(s_image)
    target_image = numpy.array(t_image)
    image_sources.append(s_image)
    image_targets.append(t_image)
    sources.append(source_image)
    targets.append(target_image)


for j in range(0, 15):
    s_mean = get_mean(0, sources[j].shape[0], 0, sources[j].shape[1], sources[j])
    t_mean = get_mean(0, targets[j].shape[0], 0, targets[j].shape[1], targets[j])
    s_std = get_std(0, sources[j].shape[0], 0, sources[j].shape[1], sources[j])
    t_std = get_std(0, targets[j].shape[0], 0, targets[j].shape[1], targets[j])
    new_sources = []
    for p in range(0, 3):
        new_sources.append(color_transfer(sources[j][:, :, p], 0, sources[j].shape[0], 0, sources[j].shape[1],
                                          s_mean[p], t_mean[p], s_std[p], t_std[p]))
    new_sources = np.dstack((new_sources[0], new_sources[1], new_sources[2]))
    Image.fromarray(new_sources).save("result1_" + str(j + 1) + ".png")


for k in range(0, 15):
    s_image_array = numpy.asarray(image_sources[k].convert("L"))
    t_image_array = numpy.asarray(image_targets[k].convert("L"))
    limits = color_transfer_according_to_ssd(s_image_array, t_image_array)
    shapes = sources[k].shape
    print(shapes)
    for lmt in range(0, len(limits)):
        s_mean = get_mean(limits[lmt][0][0], limits[lmt][0][1], limits[lmt][0][2], limits[lmt][0][3], sources[k])
        t_mean = get_mean(limits[lmt][1][0], limits[lmt][1][1], limits[lmt][1][2], limits[lmt][1][3], targets[k])
        s_std = get_std(limits[lmt][0][0], limits[lmt][0][1], limits[lmt][0][2], limits[lmt][0][3], sources[k])
        t_std = get_std(limits[lmt][1][0], limits[lmt][1][1], limits[lmt][1][2], limits[lmt][1][3], targets[k])
        print(limits[lmt])
        for p in range(0, 3):
            sources[k][:, :, p] = color_transfer(sources[k][:, :, p],
                                                 shapes[0] // 2 * (lmt // 2),  # x_start
                                                 shapes[0] // 2 * (lmt // 2) + shapes[0] // 2,  # x_finish
                                                 shapes[1] // 2 * (lmt % 2),  # y_start
                                                 shapes[1] // 2 * (lmt % 2) + shapes[1] // 2,  # y_finish
                                                 s_mean[p], t_mean[p], s_std[p], t_std[p])

    Image.fromarray(sources[k]).save("result2_" + str(k + 1) + ".png")
