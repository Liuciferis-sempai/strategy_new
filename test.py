def func(**kwargs):
    text = "aaa {kn} b {kj}"
    print(text.format(**kwargs))

func(kn="111")