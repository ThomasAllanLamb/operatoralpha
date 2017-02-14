This project provides tools to calculate and visualize [Hyperoperation](https://en.wikipedia.org/wiki/Hyperoperation). 

### Setup

Bundle the javascript:
```shell
browserify lib/main.js -o public/javascript/bundle.js
```

Generate a .csv full of the first few points (3,4,6 chosen because that's as much as my computer can handle):
```shell
python generate.py 3 4 6
```

Start the server:
```shell
node start
```

Visit [localhost:3000](http://localhost:3000)

## To use port 80

When starting the server, instead use
```shell
sudo PORT=80 node start
```


### Not yet implemented

Arbitrary operator identities. 

### Possible future features

Generalizing the domains of m and u from the set of naturals to the set of integers or reals.

### Open questions

Can n be a real value?

### To do

- API versioning
- Prevent text from highlighting when graphs are clicked
- Add transition between graphs
- Switch from storing generated points in a csv to storing generated points in a database
- Make transitions look better
- Add a paragraph explaining the meaning of the graph