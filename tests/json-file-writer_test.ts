import { IJsonFileWriter } from "../functional/large-json-writer.ts";
import { Parser } from "../data/data.ts"
import { assert } from "https://deno.land/std@0.149.0/testing/asserts.ts";

class TestJsonWriter implements IJsonFileWriter {
    wasWrittenToOnce = false;
    wasClosed = false;
    pastClosed = false;
    // deno-lint-ignore require-await
    public async writeArray <T>(_array: T[], close = false){
        this.wasWrittenToOnce = true;
        if (close && this.wasClosed){
            this.pastClosed = true;
        }
        if (close){
            this.wasClosed = true;
        }
    }

    public passesTest(): [boolean, string] {
        let errMsg = "";
        if (!this.wasClosed){
            errMsg += "Wasn't closed & "
        }
        if (this.pastClosed){
            errMsg += "Was closed twice"
        }
        return [this.wasWrittenToOnce == this.wasClosed && !this.pastClosed, errMsg];
    }
}

const testImpl = (nGroups: number, interval: number, testMain: boolean) => {
    const parser = new Parser();
    const _: number[][] = [];
    const mainTestWriter = new TestJsonWriter();
    const secondaryTestWriter = new TestJsonWriter();
    for (let i = 0; i < nGroups; i++){
        parser.write(_, nGroups, i, interval, secondaryTestWriter, mainTestWriter);
    }
    if (testMain){
        return mainTestWriter.passesTest();
    } else {
        return secondaryTestWriter.passesTest();
    }
}

const test = (nGroups: number, interval: number): void => {
    Deno.test(`${nGroups}, ${interval} \tMAIN`, () => assert(...testImpl(nGroups, interval, true)));   
    Deno.test(`${nGroups}, ${interval} \tSEC`, () => assert(...testImpl(nGroups, interval, false)));   
}

test(16,5);
test(20,10);
test(10,1);
test(10,10);
test(15,5);
test(123,12);
test(11,11);
test(111,11);
test(10,5);
test(100,14);
test(28,21);
test(6,2);