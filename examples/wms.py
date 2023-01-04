import cartopy.crs as ccrs
import matplotlib.pyplot as plt


def main():
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.InterruptedGoodeHomolosine())
    ax.coastlines()

    ax.add_wms(wms='http://vmap0.tiles.osgeo.org/wms/vmap0',
               layers=['basic'])

    plt.show()


if __name__ == '__main__':
    main()