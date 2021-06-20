import datetime

# https://www.sweclockers.com/artikel/18402-sweclockers-prestandaindex-for-grafikkort
# Fetched 2020-12-17.
# May have been moved to
# https://www.sweclockers.com/artikel/18402-sweclockers-prestandaindex-for-grafikkort/2
# Look for the variant that has Geforce RTX 2070 Super as index.
# If data is missing, then check if a recent GPU review page is more up to date.
# Here we use the numbers from the 3840x2160 diagram.
gpus = [
    {
        "name": "Nvidia Geforece RTX 3090",
        "id": "nvidia_geforce_rtx_3090",
        "label": "3090",
        "date": datetime.date(2020, 9, 24),
        "rating": 209
    },
    {
        "name": "Nvidia Geforece RTX 3080 Ti",
        "id": "nvidia_geforce_rtx_3080_ti",
        "label": "3080ti",
        "date": datetime.date(2021, 6, 3),
        "rating": 204
    },
    {
        "name": "Nvidia Geforece RTX 3080",
        "id": "nvidia_geforce_rtx_3080",
        "label": "3080",
        "date": datetime.date(2020, 9, 16),
        "rating": 187
    },
    {
        "name": "AMD Radeo RX 6900 XT",
        "id": "amd_radeon_rx_6900_xt",
        "label": "6900xt",
        "date": datetime.date(2020, 12, 8),
        "rating": 184
    },
    {
        "name": "AMD Radeo RX 6800 XT",
        "id": "amd_radeon_rx_6800_xt",
        "label": "6800xt",
        "date": datetime.date(2020, 11, 18),
        "rating": 169
    },
    {
        "name": "AMD Radeo RX 6800",
        "id": "amd_radeon_rx_6800",
        "label": "6800",
        "date": datetime.date(2020, 11, 18),
        "rating": 149
    },
    {
        "name": "Nvidia Geforece RTX 3070 Ti",
        "id": "nvidia_geforce_rtx_3070_ti",
        "label": "3070ti",
        "date": datetime.date(2021, 6, 10),
        "rating": 147
    },
    {
        "name": "Nvidia Geforece RTX 2080 Ti",
        "id": "nvidia_geforce_rtx_2080_ti",
        "label": "2080ti",
        "date": datetime.date(2018, 9, 27),
        "rating": 139
    },
    {
        "name": "Nvidia Geforece RTX 3070",
        "id": "nvidia_geforce_rtx_3070",
        "label": "3070",
        "date": datetime.date(2020, 10, 29),
        "rating": 136
    },
    {
        "name": "AMD Radeon RX 6700 XT",
        "id": "amd_radeon_rx_6700_xt",
        "label": "6700xt",
        "date": datetime.date(2021, 3, 18),
        "rating": 119
    },
    {
        "name": "Nvidia Geforece RTX 3060 Ti",
        "id": "nvidia_geforce_rtx_3060_ti",
        "label": "3060ti",
        "date": datetime.date(2020, 12, 2),
        "rating": 117
    },
    {
        "name": "Nvidia Geforece RTX 2080 Super",
        "id": "nvidia_geforce_rtx_2080_s",
        "label": "2080s",
        "date": datetime.date(2019, 6, 23),
        "rating": 116
    },
    {
        "name": "Nvidia Geforece RTX 2080",
        "id": "nvidia_geforce_rtx_2080",
        "label": "2080",
        "date": datetime.date(2018, 9, 20),
        "rating": 110
    },
    {
        "name": "AMD Radeon VII",
        "id": "amd_radeon_vii",
        "label": "VII",
        "date": datetime.date(2019, 2, 7),
        "rating": 100
    },
    {
        "name": "Nvidia Geforce RTX 2070 Super",
        "id": "nvidia_geforce_rtc_2070_super",
        "label": "2070s",
        "date": datetime.date(2019, 7, 9),
        "rating": 100
    },
    {
        "name": "Nvidia Geforce GTX 1080 Ti",
        "id": "nvidia_geforce_gtx_1080_ti",
        "label": "1080ti",
        "date": datetime.date(2017, 3, 10),
        "rating": 94
    },
    {
        "name": "Nvidia Geforece RTX 3060",
        "id": "nvidia_geforce_rtx_3060",
        "label": "3060ti",
        "date": datetime.date(2021, 2, 25),
        "rating": 92
    },
    {
        "name": "AMD Radeon RX 5700 XT",
        "id": "amd_radeon_rx_5700_xt",
        "label": "5700xt",
        "date": datetime.date(2019, 7, 7),
        "rating": 90
    },
    {
        "name": "Nvidia Geforce RTX 2070",
        "id": "nvidia_geforce_rtx_2070",
        "label": "2070",
        "date": datetime.date(2018, 10, 17),
        "rating": 86
    },
    {
        "name": "Nvidia Geforce RTX 2060 Super",
        "id": "nvidia_geforce_rtc_2060_super",
        "label": "2060s",
        "date": datetime.date(2019, 7, 9),
        "rating": 81
    },
    {
        "name": "AMD Radeon RX 5700",
        "id": "amd_radeon_rx_5700",
        "label": "5700",
        "date": datetime.date(2019, 7, 7),
        "rating": 80
    },
    {
        "name": "AMD Radeon RX Vega 64",
        "id": "amd_radeon_rx_vega_64",
        "label": "vega64",
        "date": datetime.date(2017, 8, 14),
        "rating": 77
    },
    {
        "name": "Nvidia Geforece GTX 1080",
        "id": "nvidia_geforce_gtx_1080",
        "label": "1080",
        "date": datetime.date(2016, 5, 17),
        "rating": 71
    },
    {
        "name": "AMD Radeon RX Vega 56",
        "id": "amd_radeon_rx_vega_56",
        "label": "vega56",
        "date": datetime.date(2017, 8, 28),
        "rating": 68
    },
    {
        "name": "Nvidia Geforce RTX 2060",
        "id": "nvidia_geforce_rtc_2060",
        "label": "2060",
        "date": datetime.date(2019, 1, 15),
        "rating": 60
    }
]
