def linear_interpolation(y0,y1,x0,x1,x):
    return y0 + ((y1-y0)/(x1-x0)) * (x-x0)
