Title: interface
Date: 2015-12-03 10:20
Tags: golang
Slug: golang-interfaces


```
// An Expr is an arithmetic expression.
type Expr interface {
	// Eval returns the value of this Expr in the environment env.
	Eval(env Env) float64
	// Check reports errors in this Expr and adds its Vars to the set.
	Check(vars map[Var]bool) error
}
```
