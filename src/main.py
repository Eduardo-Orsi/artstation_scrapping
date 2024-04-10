from pipeline.artist_urls import ArtistUrlPipeline
from pipeline.artist import ArtistPipeline


COOKIE = '__stripe_mid=416fff6f-8eae-422d-8580-06ffb3d83d17135936; visitor-uuid=089b8550-4eee-40f7-a8b3-6edd3d8d700d; __cf_bm=C6X..oGJLbR8M0YFwNBZlNzyo82zfO8lgMWUoHUd3Js-1712791150-1.0.1.1-PDIV8snomQ3QUvyIl4NKtnj3uAliP4LBniHz22Gdp5khfkCRAoyuCmQeao3jzz66pLF0PQI22kxgjQ1wUX3pu.8GblJfbvROxI3satMhmOc; cf_clearance=uwM1XyA9gCZjr670WMh2fxtJiSJRZJ8flMDMpnVqiDQ-1712791151-1.0.1.1-F_kIs5f.FSM3JeMChZ5NZ7KMEbZteA6FK.yaxqFT1c5pW2PpSxax2.516A1RtUGiT85h3IM0ZM4VoDAm7iAhKQ; __stripe_sid=ddebdfe1-cb3e-4f72-b8f4-25af82b0f49cee6287; g_state={"i_p":1715210357548,"i_l":4}'

if __name__ == "__main__":
    ArtistUrlPipeline.main(cookie=COOKIE)
    # ArtistPipeline.main(cookie=COOKIE)
