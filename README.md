# Omok   


    from Omok.Omok import Omok
    
    omok = Omok(LENGTH, SIZE)

---

## Omok property

|func                               |return     |description                                    |
|-----------------------------------|-----------|-----------------------------------------------|
|putStone(int x, int y, int type)   |int        |Put stone, returning integer. [-1, 0, 1, 2]    |
|isPossable(int x, int y, int type) |Bool       |Check.                                         |
|getMap()                           |int[][]    |Return 2d array.                               |
