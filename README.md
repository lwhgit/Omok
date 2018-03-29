# Omok   


    from Omok.Omok import Omok
    
    omok = Omok(LENGTH, SIZE)

or

    from Omok.Omok import Omok
    
    omok = Omok(LENGTH)
---

## Omok property

|func                               |return     |description                                    |
|-----------------------------------|-----------|-----------------------------------------------|
|putStone(int x, int y, int type)   |int        |Put stone, returning integer. [-1, 0, 1, 2]    |
|isPossable(int x, int y, int type) |Bool       |Check.                                         |
|getMap()                           |int[][]    |Return 2d array.                               |
|reset()                            |void       |Reset map.                                     |
|get3DArray()                       |int[][][]  |Return 3d array.                               |
|userInput()                        |int        |Receive users input and return result          |
