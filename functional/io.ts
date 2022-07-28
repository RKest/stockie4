interface IO {
  write: (path: string, data: string) => Promise<void>;
  append: (path: string, data: string) => Promise<void>;
  read: (path: string) => Promise<string>;
  // deno-lint-ignore ban-types
  readJson: <T extends object>(path: string) => Promise<T>;
  // deno-lint-ignore ban-types
  writeJson: (path: string, data: object) => Promise<void>;
  exists: (path: string) => Promise<boolean>;
  remove: (path: string) => Promise<void>;
}

const decoder = new TextDecoder("utf8");
const encoder = new TextEncoder();

const read = async (path: string): Promise<string> => {
  const bytes = await Deno.readFile(path);
  return decoder.decode(bytes);
};

const write = async (path: string, data: string) => {
  const bytes = encoder.encode(data);
  await Deno.writeFile(path, bytes);
};

const append = async (path: string, data: string) => {
  const bytes = encoder.encode(data);
  await Deno.writeFile(path, bytes, { append: true });
};

const readJson = async (path: string) => {
  const jsonString = await read(path);
  return JSON.parse(jsonString);
};

// deno-lint-ignore ban-types
const writeJson = async (path: string, data: object) => {
  const jsonString = JSON.stringify(data, null, 2);
  await write(path, jsonString);
};

const exists = async (path: string) => {
  try {
    await Deno.stat(path);
    return true;
  } catch (error) {
    if (error instanceof Deno.errors.NotFound) {
      return false;
    } else {
      throw error;
    }
  }
};
const remove = async (path: string) => {
  await Deno.remove(path);
};
export const io: IO = {
  read,
  write,
  append,
  readJson,
  writeJson,
  exists,
  remove,
};
