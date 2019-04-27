/****************************************************************************
 *  Author: Andrew Osborne
 *  Date: March 29, 2019
 * 
 * INFO:
 *  This file implements a solution to the modified activity selection 
 *  problem in accordance with the seventh programming assignment in 
 *  CSCE 4013 Algorithms. At a high level, I have created a class
 *  Activity, which will store a single activity, with all of its data
 *  and a class, ActivityList, which is effectively an array of 
 *  Activities with some metadata. 
 *
 *  Then, I use a dynamic programming approach to populate two paralell arrays
 *  in order of increasing difference with optimal solutions to subproblems
 *  while handling the problem of uniqueness with relatively little extra 
 *  overhead.
 ****************************************************************************/

import java.io.File;
import java.util.Scanner;
import java.util.Arrays;
import java.io.PrintWriter;

class Activity
{
  // This class is used to store activities from the input file.
  // A single instance of this class can store a single activity

  public int id;
  public int value;
  public int lb;
  public int ub;

  // This constructor is quite simple, and it is the only one actually used
  Activity(int id, int lb, int ub, int value)
  {
    this.id = id;
    this.lb = lb;
    this.ub = ub;
    this.value = value;
  }

  // the purpose of this constructor is to ruin the computation if any 
  // activity is accidentally initialized incorrectly
  Activity()
  {
    this.id = -1;
    this.value = -1;
    this.lb = -1; 
    this. ub = -1;
  }

  // this is for testing purposes only
  void show()
  {
    String id = Integer.toString(this.id);
    String val = Integer.toString(this.value);
    String lb = Integer.toString(this.lb);
    String ub = Integer.toString(this.ub);

    System.out.println(id + " " + lb + " " + ub + " " + val);

  }

}

class ActivityList
{
  // This class is essentially an array of Activities with some additional
  // metadata. This is the primary datastructure used in computation

  // this is the upper bound of the interval [0, U] on which activities may be sceduled
  private int upperBound;

  // the total number of tasks passed into ActivityList() from the input file
  private int numTasks;

  // all integer values must be less than this value 
  static final int maxVal = 100000;

  // this is an array to be sorted in order of increasing finish time
  public Activity [] actList;

  // the purpose of this array is to shorten the code when an ID of some
  // activity is required. This is non--essential to the algorithm and 
  // used only for convenience 
  public int [] idMap;
  
  ActivityList(String filename)
  {
    // parse the input file and store metadata, 
    // then sort this.actList in order of increasing finish time

    File input = new File(filename);
    Scanner sc;

    // if this file does not exist, an exception will be thrown
    try
    {
      sc = new Scanner(input);
    }
    catch(Exception e)
    {
      throw new RuntimeException("You have typed the input filename incorrectly");
    }

    this.numTasks = sc.nextInt();
    this.upperBound = sc.nextInt();
    
    this.actList = new Activity[this.numTasks+2];
    int i = 0;
    
    // add two ficticious activities, one of which ends at zero, and the other 
    // begins  at this.numTasks + 1
    this.actList[0] = new Activity(0,-1,0,0);
    this.actList[numTasks+1] = new Activity(numTasks+1,this.upperBound,this.upperBound + 1,0);
    
    // used to temporarily store values from input fie
    int id;
    int lb;
    int ub;
    int val;

    while(sc.hasNextInt())
    {
      id = sc.nextInt();
      lb = sc.nextInt();
      ub = sc.nextInt();
      val = sc.nextInt();
      this.actList[id] = new Activity(id,lb,ub,val);
      i += 1;
    } 

    // sort in order of increasing finish time 
    this.increasingFinishSort();
  }

  int getNumTasks()
  {
    return this.numTasks;
  }

  void increasingFinishSort()
  {
    // uses insertion sort to ensure that ActivityList is sorted in 
    // order of increasing finish time
    //
    // note that the worst-case runtime of this algo is O(n^2)
    // which is does not affect our runtime asymptotically because
    // our asymptotic runtime is w(n^2)

    this.idMap = new int[this.numTasks+2];
    Activity [] sorted = new Activity[this.numTasks+2];
    sorted[0] = this.actList[0];
    sorted[this.numTasks+1] = this.actList[this.numTasks+1];
    this.idMap[0] = 0;
    this.idMap[this.numTasks+1] = this.numTasks+1;

    Activity temp;
    int tempint;
    
    // insertion sort
    for (int i = 2; i <= this.numTasks; i++)
    {
      this.idMap[i] = this.actList[i].id;

      for (int j = i ; j > 1 ; j--)
      {
        if (this.actList[j].ub < this.actList[j-1].ub)
        {
          temp = this.actList[j];
          this.actList[j] = this.actList[j-1];
          this.actList[j-1] = temp;
        }
      }
    }

    // update the id-map to preserve id ordering
    for (int i = 0; i < this.numTasks +2; i++)
      this.idMap[i] = this.actList[i].id;
  }
 
  // for testing purposes only 
  void show()
  {
    String num = Integer.toString(this.numTasks);
    String upper = Integer.toString(this.upperBound);
    System.out.println(num + " " + upper);
    for (int i = 0 ; i < this.numTasks+2; i++)
      this.actList[i].show();

  }

  int getId(int i)
  {
    return this.idMap[i];
  }

}


class ActivityPlanner
{
  // this class is used to solve the problem at hand using previously
  // defined data structures


  // this will contain optimal values, that is c[i][j] contains the value of the
  // optimally scheduled activities between activity i and activity j
  public  int [][] c;

  // this contains data necessary to reconstruct the optimal schedule
  // path[i][j] contains the activity which should be scheduled 
  // between activity and activity j.
  //
  // path and c satisfy:
  //      c[i][j] = c[i][path[i][j]] + c[path[i][j]][j] + this.data[path[i][j]].value
  // at the end of computation, and this fact is used to ascertain the uniqueness
  // of our solution
  public  int [][] path;
  public  int size;

  // this stores the activities
  private ActivityList data;

  ActivityPlanner(String filename)
  {
    // read data into this.data, initialize this.c and this.path
    this.data = new ActivityList(filename);
    this.size = this.data.getNumTasks();
    this.c = new int[size+2][size+2];
    this.path = new int[size+2][size+2];
  }

  boolean []  solve()
  {
    // this is the beef of our algorithm
    
    // index values
    int k;
    int l;

    // used to limit unnecessary array accesses
    int flag = 0;

    // this array is used, in the last iteration of the loop over i
    // so that, after the computation, any index i for which flags[i] == 1
    // i would yield the same optimal solution as the value in path[0][n+1]
    boolean [] flags = new boolean[this.size+2];

    // this outer loop iterates over the difference in order-statistic between
    // elements in our this.data.
    //
    // that is, we first find the optimal activity to lie between 0 and the start time
    // of activity 2 (indexed by finish time). The only possible choice for this 
    // is activity one. This interval shifts until the outer loop iterates.
    //
    // at each iteration of this loop we will solve n - i subproblems of size i
    // for a total sum of O(n^3) checks. This is explained in more detain in my report
    for (int i = 2 ; i< this.size+2 ; i++)
    {
      // this loop shifts the lower and upper bounds of our search window
      for(int j = 0; j < this.size+2-i; j++)
      {
        k = j+i;
        l = k-1;
        while(this.data.actList[j].ub < this.data.actList[l].ub)
        {
          // proposed value of c[j][k] 
          flag = this.c[j][l] + this.c[l][k] + this.data.actList[l].value; 

          // if activity l fits within activity j and activity k
          if (( this.data.actList[j].ub <= this.data.actList[l].lb) &&
                (this.data.actList[l].ub <= this.data.actList[k].lb))
          {
            // if proposed value exceeds current value of c[j][k]
            if(flag > this.c[j][k])
            {
              // this checks to see if we are in the final iteration of our program
              if (j==0 && k == this.size+1)
              {
                // if we are in our last iteration and the optimal value is updated, 
                // clear flag, because the current solution is the only optimal solution
                // currently found
                for (int n = 0; n < this.size+2; n++)
                  flags[n] = false;

                flags[l] = true;
              }

              this.c[j][k] = flag;
              this.path[j][k] = l;
            }
            else if (flag == this.c[j][k])
              // if we are in our last iteration and we have found a value which 
              // is equal to our optimal solution, this is a candidate for 
              // an alternative solution
              if (j==0 && k == this.size+1)
                flags[l] = true;
          }
          l -= 1;
        } 
      }
    }
    return flags;
  }

  int getId(int i, int j)
  {
    return this.data.getId(this.path[i][j]);
  }

  // for testing purposes only
  void printSolution()
  {
    System.out.println("solution"); 
    System.out.println(this.c[0][this.size+1]);
    System.out.println("C matrix");
    System.out.println(Arrays.deepToString(this.c).replace("],","\n"));
    
    System.out.println("\n" + this.activities());
    System.out.println("path matrix");
    System.out.println(Arrays.deepToString(this.path).replace("],","\n"));

  }

  // for testing purposes only
  String activities()
  {
    String activities = "";
    for (int i = this.size + 1; i > 0;)
    {
      if (this.path[0][i] != 0)
        activities = Integer.toString(this.getId(0,i))+" " + activities;
      i = this.path[0][i];
    }

    return activities;
  }

  // this function checks if our solution is unique based on the 
  // flag array returned from solve()
  boolean  isUnique(boolean [] flags)
  {
    // worst-case runtime O(n)
    //
    // this array stores the optimal schedule reported by solve()
    int [] opt = this.sortedSolution(this.path[0][this.size+1]);

    // do not check any duplicates of the reported solution
    for (int k = 0; k < opt.length; k++)
      flags[opt[k]] = false;

    // this is a temporary used to store potentially optimal solutions
    // which are to be compared to the reported optimal solution
    int [] comp;

    for (int i = 0; i < flags.length; i++)
    {
      // flags[i] == true
      if (flags[i])
      {
        comp = this.sortedSolution(i);

        // if proposed solution is not the same length
        // of reported solution, they cannot be equal
        if (comp.length != opt.length)
          return false;
        else
        {
          // if a single element differs between the proposed
          // and reported solutions differ, they cannot be the same
          for (int j = 0 ; j < opt.length;j++)
            if (opt[j] != comp[j])
              return false;
        }
      }
    }
    return true;
  }


  String altPrint(int i, int j,int repl)
  { 
    // this function generates a string of integers 
    // delimited by spaces which contain the activities in
    // an optimal schedule between activities i and j
    //
    // if repl > 0, then this computes the same string
    // but in the case that this.path[i][j] = repl
    // Used to generate strings of schedules which are potentially
    // optimal
    int k = (repl > 0 ? repl: this.path[i][j]);
    String Soln = "";
    
    if (k  > 0 )
    {
      Soln += Integer.toString(this.data.getId(k))+ " "; 
      Soln += this.altPrint(i,k,0) + " ";
      Soln += this.altPrint(k,j,0) + " ";
    }
    
    return Soln;
  }


  int [] sortedSolution(int l)
  {
    // create a sorted array of integers representing 
    // the schedule if the optimal activity to be scheduled first
    // is activity l
    
    // get activity string
    String s = this.altPrint(0,this.size+1,l);

    // split activity string by spaces
    // multiple spaces are a single delimiter
    String [] splt = s.split("[ ]+");

    // used to store the returned array
    int [] arr = new int[splt.length];
    for (int i = 0; i < arr.length; i++)
    {
      // convert string into integer. 
      // Will throw an exception if string is not an int
      try{
        arr[i] = Integer.parseInt(splt[i]);
      }
      catch(Exception e)
      {
        // this will cause obvious problems later
        arr[i] = -1;
      }
    }
    
    int temp = 0;
    // insertion sort
    for (int j = 1; j < arr.length; j++)
    {
      for (int k = j; k > 0; k--)
      {
        if ( arr[k] < arr[k-1])
        {
          temp = arr[k];
          arr[k] = arr[k-1];
          arr[k-1] = temp;
        }
      }
    }  

    return arr;
  }
}


public class Homework7
{
  public static void main(String[] args)
  {
    // read problem from args[0], generate formatted output, and write 
    // it to args[1], creating args[1] if it does not exist.
    ActivityPlanner soln = new ActivityPlanner(args[0]);
    boolean [] flags = soln.solve();
    for (int i = 0 ; i < flags.length; i++)
      if (flags[i])
        System.out.println(Arrays.toString(soln.sortedSolution(i)));

    String send = "";
    send += Integer.toString(soln.c[0][soln.size+1]) + "\n";
    int [] sortedArrayOfSolution = soln.sortedSolution(soln.path[0][soln.size+1]);
    for (int i = 0; i < sortedArrayOfSolution.length; i++)
      send += Integer.toString(sortedArrayOfSolution[i]) + " ";
    send += "\n";

    if (soln.isUnique(flags))
      send += "IT HAS A UNIQUE SOLUTION";
    else 
      send += "IT HAS MULTIPLE SOLUTIONS";

    try{
      //System.out.println(send);
      File outfile = new File(args[1]);
      outfile.createNewFile();
      PrintWriter out = new PrintWriter(outfile);
      out.print(send);
      out.close();
    }
    catch(Exception e)
    {
      System.out.println("This program does not have permission to create files, and the file passed as a second command argument does not exist");
    }
  }
}
