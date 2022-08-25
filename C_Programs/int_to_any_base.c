#include <stdio.h>
#include <unistd.h>
#include <string.h>

void ft_putnbr_base(int nbr, char *base)
{
    int base_size;
    int i;
    int x;

    base_size = 0;
    while (base[base_size] != '\0')
    {
        base_size++;
    }
    char array[nbr/base_size + 1];

    i = 0;
    while (nbr > 0)
    {
    x = nbr % base_size;
    nbr = (nbr - x) / base_size;
    x = base[x];
    array[i] = x;
    i++;
    write(1, &x, 1);
    }  
    printf("\n");
    while (i >= '\0')
    {
        write(1, &array[i], 1);
        i--;
    }
    
}

int main()
{
    char s2[40] = "01";
    ft_putnbr_base(2135234,s2);
    return 0;
}
