import { io } from "./io.ts";

interface JsonFileWriterOptions {
    doStrip?: boolean;
    isArray?: boolean;
}

export interface IJsonFileWriter {
    writeArray: <T>(array: T[], close: boolean) => Promise<void>;
}
export default class JsonFileWriter implements IJsonFileWriter {
    path: string;
    isArray: boolean;
    doStrip: boolean;
    isInitialised = false;
    private append = async (data: string) => await io.append(this.path, data);
    constructor(path: string, options: JsonFileWriterOptions) {
        this.path = path;
        this.isArray = options.isArray ?? true;
        this.doStrip = options.doStrip ?? false;
    }
    
    public async writeArray<T>(array: T[], close = false) {
        if (!this.isInitialised){
            if (this.isArray){
                await this.append('[');
            } else {
                await this.append('{');
            }
            this.isInitialised = true;
        }
        let arrayString = JSON.stringify(array, null, 2);
        if (this.doStrip){
            arrayString = arrayString.slice(1, -1);
        }
        // console.log(array);
        await this.append(arrayString);
        if (!close){
            await this.append(',');
        } else if (this.isArray) {
            await this.append(']');
        } else {
            await this.append('}');
        }
    }
}