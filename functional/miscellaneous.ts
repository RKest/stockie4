export { getRandomString, avgerageArray, groupArray }

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

const groupArray = <T>(arr: T[], groupSize = 100): T[][] => {
    const groups: T[][] = []
    for (let i = 0; i < arr.length; i += groupSize){
        groups.push(arr.slice(i, i + groupSize));
    }
    return groups;
}
