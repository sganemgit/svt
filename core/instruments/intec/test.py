
import inspect 
import libIntec.libIntec as intec
os.path.append(inspect(intec))


if __name__=="__main__":
    import time
    print(GetlibVersion())
    Initialize()
    InitializeCard(0)
    set_temp = 25 
    SetTemperature(0, 0, set_temp)
    temp = GetTemperature(0, 0)

    print(temp["temperature"])
    while temp["temperature"] < set_temp - 0.5 or temp["temperature"]  > set_temp + 0.5:
        temp = GetTemperature(0, 0)
        print(temp["temperature"])
        time.sleep(1)
    Exit()

