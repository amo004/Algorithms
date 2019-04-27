import java.util.Random;

/*******************************************************************************
  Author: Andrew Osborne
  Date: March 7, 2019

  This file implements the insertion method of a hash table using open
  addressing with multiple probing functions as required in homework assignment
  five.


*******************************************************************************/

class HashTable
{
  // keeps track of size of the table
  private int size;

  //array keeping track of keys in the hash table
  public int [] table;

  // if occupied[index] == true, then we have inserted
  // a key which landed in occupied[index]
  private boolean [] occupied;

  // this flag is used to determine what kind of probing to do
  //  0 - linear probing
  //  1 - quadratic probing
  //  2 - double hashing
  private int hash;

  HashTable(int size, int hash)
  {
    this.size = size;

    // allocate data arrays
    this.table = new int[size];
    this.occupied = new boolean[size];
    for (int i = 0; i < size; i++)
    {
      this.table[i] = -1;
      this.occupied[i]=false;
    }

    // used as a flag to determine which hashing function to use
    if ((hash < 0) || (hash>2))
      throw new RuntimeException("invalid hash value"); // sanitize flag value

    this.hash = hash;

  }

  private int linearProbe(int key, int i)
  {
    return (key + i)%this.size;
  }

  private int quadraticProbe(int key, int i)
  {
    return (key + i + 3*i*i)%this.size;
  }

  private int doubleHash(int key, int i)
  {
    int h2 = 1 + (key % (this.size-1) );
    return (key + i*h2)%this.size;
  }

  // this function abstracts away the logic of choosing which probing function
  // to use. Uses this.hash to make decision internally
  private int hashV(int key, int i)
  {
    if (this.hash==0)
      return this.linearProbe(key,i);
    else if (this.hash == 1 )
      return this.quadraticProbe(key,i);
    else if (this.hash == 2)
      return this.doubleHash(key,i);
    return -1;
  }

  public int insert(int key)
  {
    int location;
    for (int i = 0 ; i < this.size; i++)
    {
      // evaluate the hash function
      location = this.hashV(key,i);

      // if we find an empy spot, quit the loop
      if (!this.occupied[location])
      {
        // insert element into table
        this.table[location] = key;

        // record that table[location] is occupied
        this.occupied[location]=true;

        // return number of probes into table
        return i+1;
      }
    }
    System.out.println("HEAP OVERFLOW" + " key:" + key + " hash:" + this.hash);
    // error flag : HEAP OVERFLOW
    return -1;
  }

  public int search(int key)
  {
    int location;
    for (int i = 0; i < this.size; i++)
    {
      location = this.hashV(key,i);

      if (this.occupied[location] == true)
      {
        if (this.table[location] == key)
          return location; // return index of found element
      }
      else // if we found empty spot, quit the program, search failed
        return -1;
    }
    return -1;
  }


}

public class Homework5
{

  public static void main(String[] args)
  {
    int maxNum = 100000;
    Random rand = new Random();


    HashTable a = new HashTable(1009,0); // linear probing
    HashTable b = new HashTable(1009,1); // quadratic probing
    HashTable c = new HashTable(1009,2); // double hashing

    // used as a temporary value to generate a random number which is in
    // none of the hash tables
    int toBeInserted = rand.nextInt(maxNum);

    // for 900 elements, find an int not in the table and insert it
    //  into all three tables
    for (int k = 0 ; k <= 900; k++)
    {
      // search returns the index of the found element
      // or -1 if it is not found
      while (c.search(toBeInserted) >= 0)
        toBeInserted = rand.nextInt(maxNum);

      a.insert(toBeInserted);
      b.insert(toBeInserted);
      c.insert(toBeInserted);
    }

    // keeping track of how many probes completed for last 50 elems
    int aProbes = 0;
    int bProbes = 0;
    int cProbes = 0;

    // follow the same procedure as above to find elements not in the
    // table which are to be inserted
    // Note that the same elements wind up in each table
    for (int k = 0 ; k <= 50; k++)
    {
      // search returns the index of the found element
      // or -1 if it is not found
      while (c.search(toBeInserted) >= 0)
        toBeInserted = rand.nextInt(maxNum);

      aProbes += a.insert(toBeInserted);
      bProbes += b.insert(toBeInserted);
      cProbes += c.insert(toBeInserted);
    }

    // print results
    System.out.println("Number of probes for last fifty elements inserted (linear probing) " + aProbes);
    System.out.println("Number of probes for last fifty elements inserted (quadratic probing) " + bProbes);
    System.out.println("Number of probes for last fifty elements inserted (double hashing) " + cProbes);
  }
}
