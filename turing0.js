function isPalindrome(word)
{
  word = word.toLowerCase();
  
  // Please write your code here.
  for (let i = 0; i < word.length / 2; i++)
    if (word.charCodeAt(i) !== word.charCodeAt(word.length - i - 1))
      return false;
  
  return true
}
var word = readline()
print(isPalindrome(word))
