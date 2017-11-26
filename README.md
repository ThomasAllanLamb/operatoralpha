This project provides tools to calculate and visualize [Hyperoperation](https://en.wikipedia.org/wiki/Hyperoperation). 

### Setup

Bundle the javascript:
```shell
browserify lib/main.js -o public/javascript/bundle.js
```

Generate a .csv of some points. (these parameters are about as much as my computer can handle):
```shell
python generate-bounded.py -5 1 1 6 7 3 10
```

Start the server:
```shell
node ./bin/www
```

Visit [localhost:3000](http://localhost:3000)


## To specify hostname or port

Start with:
```shell
HOSTNAME=myHostname PORT=myPort node ./bin/www
```

### To do

- Arbitrary operator identities
- Generalizing the domains of m and u from the set of naturals to the set of integers or reals.
- API versioning
- Prevent text from highlighting when graphs are clicked
- Switch from storing generated points in a csv to storing generated points in a database
- Add a paragraph explaining the meaning of the graph
- Node start is not working on production
- Generalize n to numbers which are not positive integers
- Generalize m to rationals