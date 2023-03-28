
def get_lstm_one_surface_data(sampling, surface_name, repid_times=12):
    speeds = [10, 20, 30]
    for i in range(repid_times):
        if i % 3 == 0 and i != 0:
            input("请旋转一下表面: ")
        elif i != 0:
            input("请移动一下表面: ")
        save_name = surface_name

        sampling.goback_goback_continuous_batch(speeds, save_name=save_name)


def get_lstm_all_surface_data(sampling):
    for i in range(8):
        input("请放置No%d表面: " % i)

        get_lstm_one_surface_data(sampling, "NO%dSurface"%i)


