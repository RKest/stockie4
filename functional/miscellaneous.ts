export { getRandomString, avgerageArray }

function getRandomString(len: number): string{
    const sampleString = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM';
    const randomIndex = (): number => Math.floor(Math.random() * len);
    let returnString = '';
    for(let i = 0; i < len; i++)
        returnString += sampleString[randomIndex()];
    return returnString;
}

const avgerageArray = (arr: number[]): number => 
    arr.map(Number).reduce((acc, el) => acc + el, 0) / arr.length;
