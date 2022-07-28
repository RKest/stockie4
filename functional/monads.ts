export { Chain }

class Chain {
    value: unknown;
    constructor(value: unknown){
        this.value = value;
    }
    bind(func: (inp: unknown) => unknown){
        this.value = func(this.value);
        return this;
    }
}