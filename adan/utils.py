def get_total_seconds(time):
    return time.hour*3600+time.minute*60+time.second

def get_time_near_prayer(date_now_seconds,elfajer,duhr,alasr,almaghreb,alaicha):
    total_seconds_elfajer =  get_total_seconds(elfajer)-date_now_seconds
    total_seconds_duhr = get_total_seconds(duhr)-date_now_seconds
    total_seconds_alasr = get_total_seconds(alasr)-date_now_seconds
    total_seconds_almaghreb = get_total_seconds(almaghreb)-date_now_seconds
    total_seconds_alaicha = get_total_seconds(alaicha)-date_now_seconds
    dectinary_prayer = {
        f"{abs(total_seconds_elfajer)}":"elfajer",
        f"{abs(total_seconds_duhr)}":"duhr",
        f"{abs(total_seconds_alasr)}":"alasr",
        f"{abs(total_seconds_almaghreb)}":"almaghreb",
        f"{abs(total_seconds_alaicha)}":"alaicha"
    }
    min_time = min(abs(total_seconds_elfajer),abs(total_seconds_duhr),abs(total_seconds_alasr),abs(total_seconds_almaghreb),abs(total_seconds_alaicha))
    print(min_time)
    print(dectinary_prayer[f"{min_time}"])
    hour = int(min_time/3600)
    minutes = int((min_time/60)%60)
    secondes = int(min_time%60)
    return f"{hour}:{minutes}:{secondes}",dectinary_prayer[f"{min_time}"]