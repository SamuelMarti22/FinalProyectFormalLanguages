# Final Project - Syntactic Analyzer Type LL(1) AND SLR(1) 📖

In this assignment, the step-by-step process of analyzing a set of strings using two types of syntactic analyzers will be demonstrated: LL(1) (top-down parser) and SLR(1) (bottom-up parser). The process includes everything from identifying the type of grammar, constructing the parsing tables and automaton, to validating the strings.

## Contents 🤔

- [Team 👥](#team)
- [Development Environment 🖥️](#development-environment)
- [Instructions for Running ▶️](#instructions-for-running)
- [Video running the project ▶️](#video-running-the-project)
- [LL(1) Top-Down Parser 📝](#ll1-top-down-parser)
    - [Explanation of the Parser 📖](#explanation-of-the-parser)
    - [Code for Developing It 💻](#code-for-developing-it)
- [SLR(1) Bottom-Up Parser 🔽](#slr1-bottom-up-parser)
    - [Explanation of the Parser 📚](#explanation-of-the-parser-1)
    - [Code for Developing It 🧑‍💻](#code-for-developing-it-1)
- [General Code 🧑‍💻](#general-code)

## Team 👥

- **Team Members**: Laura Andrea Castrillón Fajardo - Samuel Martínez Arteaga

## Development Environment 🖥️

- **Operative System:** Windows 11  
- **Programming language:** Python 3.12  
- **Tools:** Visual Studio Code, Graphviz
- **Required Libraries**: Pandas, Graphviz

## Instructions for running ▶️🏃‍♂️

- 1. Install pandas. To do this, type the following command in the terminal:
```
pip install pandas
```
- 2. Install Graphviz. To do this, type the following command in the terminal:
```
sudo apt-get update
sudo apt-get install graphviz
pip install graphviz
```
- 3. Run the main file
 
## Video running the project 🧑‍💻

In the following link you will find the explanatory video of the functional code: https://drive.google.com/file/d/1fwQrTOo0MVMP2OyuH7ovXwhJu7evGD0p/view?usp=sharing
 
## Prerequisites 

The Rule class is used to represent the production rules of a grammar. Each rule consists of a left-hand side (LHS) and a right-hand side (RHS), which are essential components in formal grammar representation. The Rule class is defined as follows:
```
class Rule:
    def __init__(self,simboloProduccion,producion):
        self.simboloProduccion = simboloProduccion
        self.produccion = producion
        self.first = None
```

Based on a .txt file, this code identifies the production rules, as well as the terminal and non-terminal symbols of a given grammar. It first reads the number of rules, then processes each one by checking its format and separating the production symbol from its derivation. It also sets the start symbol and stores each rule. Finally, it reads the input strings to be analyzed until it encounters a line with the character e, which marks the end of the input:

```
rules = []
strings = []
terminals = ['$']
nonTerminals = []

#Read the input file
with open("input.txt", "r") as file:
    #Read the first line of the file, which contains the number of rules
    num_rules = int(file.readline().strip())
    #Read each rule and store it in the rules list
    for i in range(num_rules):
        rule = file.readline().strip()
        parts = rule.split("->")
        #Confirm that the rule has the correct format (Production symbol -> Production).
        if len(parts) == 2:
            parts = [parte.strip() for parte in parts]
        else:
            print("Does not meet the requirements of the txt file")
            exit()
        #Separate the different productions of the same production symbol and store them in the rules list.
        parts[1] = parts[1].split(" ")
        if i == 0:
            #Define the start symbol of the grammar.
            startSymbolGrammar = parts[0]
        #Identify the terminal and non-terminal symbols and add them to their respective lists.
        for j in range(len(parts[1])):
            identify_terminal(parts[0])
            identify_terminal(parts[1][j])
            rule = Rule(parts[0], parts[1][j])
            rules.append(rule)
    #Read the strings to process and store them in the list of strings, until the character "e" is found.
    for line in file:
        line = line.strip()+"$"
        if line == "e$":
            break
        strings.append(line)
```
The identify_terminal function analyzes each production rule to categorize symbols as either terminal or non-terminal. It iterates through each character in the production: if the character is uppercase and hasn’t been added to the nonTerminals list, it is classified as a non-terminal. If the character is not uppercase (i.e., a terminal) and hasn’t been added to the terminals list, it is added as a terminal. This process ensures that symbols are uniquely categorized and stored, distinguishing between terminals and non-terminals in the grammar.

```
#Identify terminals and non terminals of grammar in each production.
def identify_terminal(production):
    for i in range(len(production)):
        #Take each character, evaluate if it is capital and has not been add in nonTerminals.
        if production[i].isupper() and production[i] not in nonTerminals: 
            nonTerminals.append(production[i])
        # If it not is capital then this character neither is non Terminal nor it is repet in terminals. Add this character in terminals.
        elif production[i] not in nonTerminals and production[i] not in terminals:
            terminals.append(production[i])
```         

To understand parsers, it's essential to work with the production rules of a grammar and the concepts of FIRST (the set of terminals that can appear at the beginning of a derivation from a non-terminal) and FOLLOW (the set of terminals that can appear immediately after a non-terminal in a production). These sets serve as the foundation for building the parsing tables used by different types of parsers.

```
diccFirst = {}
diccFollow = {}
for i in range(len(nonTerminals)):
    diccFirst[nonTerminals[i]] = []
    diccFollow[nonTerminals[i]] = []
    if nonTerminals[i] == startSymbolGrammar:
        diccFollow[nonTerminals[i]].append("$")

#Construction the first for every non terminal.
def first(production,diccFirst,flagLL):
    #Take the first character in the production of a rule.
    symbol = production.get_production()[0]
    #If the symbol is same the symbol of the production, then in the rule exist left recursion. Not is a grammar type LL(1).
    if symbol == production.get_production_symbol():
        print("Left Recursion")
        flagLL = False
        production.set_first(".")
    else:
        #If the symbol is a non-terminal, it adds it to the first of the production symbol unless it is repeated.
        if symbol in terminals:
            production.set_first(symbol)
            if symbol not in diccFirst[production.get_production_symbol()]:
                diccFirst[production.get_production_symbol()].append(symbol)
            else:
                flagLL = False
        else:
            #If the symbol is a non-terminal, it is necessary to add the symbols from the first of that non-terminal to the first of the production symbol.
            production.set_first(diccFirst[symbol])
            if symbol not in diccFirst[production.get_production_symbol()]:
                diccFirst[production.get_production_symbol()].extend(diccFirst[symbol]) 
                #Remove the duplicate symbols after adding the corresponding first symbols of the other symbol.
                diccFirst[production.get_production_symbol()] = list(set(diccFirst[production.get_production_symbol()])) 
    return flagLL
```
This function computes the First set for a given production and checks whether the grammar is valid for LL(1) parsing. It analyzes the first symbol of the production: if it's the same as the production's head, it detects left recursion and marks the grammar as not LL(1). If the symbol is a terminal, it adds it directly to the First set. If it's a non-terminal, it appends the First set of that symbol to the current one, ensuring no duplicates. Finally, it returns a flag indicating whether the grammar remains valid for LL(1) parsing.

```
#Construction of follow for each non-terminal.
def follow(diccFollow,nonTerminal):
    for i in range(len(rules)):
        #Find in each rule if it is part of it.
        if nonTerminal in rules[i].get_production():
            positionNonTerminal = rules[i].get_production().index(nonTerminal) #Toma la posicion donde se encuentra el non terminals.
            #If the symbol is at the end of the production
            if positionNonTerminal == len(rules[i].get_production())-1: 
                #If the rule only has the non-terminal symbol as production, add the follow symbols of this non-terminal.
                if rules[i].get_production_symbol() == nonTerminal:
                    diccFollow[nonTerminal].extend(diccFollow[rules[i].get_production_symbol()])
                #If the follow of that non-terminal symbol is defined and different from '$', add its value to the follow of the symbol in the rule where it is located.
                elif diccFollow[rules[i].get_production_symbol()] != [] and diccFollow[rules[i].get_production_symbol()] != ["$"]:
                    diccFollow[nonTerminal].extend(diccFollow[rules[i].get_production_symbol()])
                #If the production is different from the non-terminal symbol, it means it does not have a follow defined yet; recursion is done to define it and then add it
                elif rules[i].get_production_symbol() != nonTerminal:
                    diccFollow[nonTerminal].extend(follow(diccFollow, rules[i].get_production_symbol()))
                diccFollow[nonTerminal] = list(set(diccFollow[nonTerminal])) #Remove the duplicate characters after adding them.
            #If the non-terminal symbol is not at the end and is followed by a terminal, add this character to the follow list of the non-terminal symbol.
            elif rules[i].get_production()[positionNonTerminal+1] in terminals:
                diccFollow[nonTerminal].append(rules[i].get_production()[positionNonTerminal+1])
                diccFollow[nonTerminal] = list(set(diccFollow[nonTerminal]))  #Remove the duplicate characters after adding them.
            else:
                #If the symbol is not at the end and is followed by a non-terminal, then it should add the elements from the first of that non-terminal.
                firstNext = diccFirst[rules[i].get_production()[positionNonTerminal+1]].copy()
                #If the first includes the symbol e, then it should remove it.
                if "e" in firstNext:
                    firstNext.remove("e")
                    if diccFollow[rules[i].get_production()[positionNonTerminal+1]] != []:
                        #If there is a follow for this non-terminal, then it adds it.
                        firstNext.extend(diccFollow[rules[i].get_production()[positionNonTerminal+1]]) 
                    else:
                        #If there is no follow for this non-terminal, then it should perform recursion to find it and add it.
                        firstNext.extend(follow(diccFollow, rules[i].get_production()[positionNonTerminal+1])) 
                #Add the first to the follow of the non-terminal and remove the duplicate characters.
                diccFollow[nonTerminal].extend(firstNext)
                diccFollow[nonTerminal] = list(set(diccFollow[nonTerminal]))
    return diccFollow[nonTerminal] 
```
The follow function constructs the Follow set for a given non-terminal symbol in a grammar. It iterates over the production rules to check if the non-terminal appears in the right-hand side of any rule. If the non-terminal is found at the end of the production, it adds the Follow set of the non-terminal’s production symbol to its own Follow set. If the non-terminal is followed by a terminal symbol, that terminal is added to the Follow set. If followed by another non-terminal, it adds the First set of that non-terminal to the Follow set, handling special cases like epsilon (e) and recursing if necessary. Duplicate elements are removed to ensure unique entries. This process helps build the Follow set for each non-terminal symbol based on the grammar's rules.

## LL(1) Top-Down Parser 📝

### Explanation of the Parser 📖

The LL(1) parser is a **top-down** parsing method that reads input from **left to right**, constructing the parse tree from **top to bottom** using **one lookahead symbol** to make decisions.

### Code for Developing It 💻

Here you would add your code that implements the LL(1) parsing algorithm.

      a\ B\ x \\
     |\\
     aa\ \ \ 
\end{array}
$$

In this example, we start from the initial symbol **S**, which produces **A B X**. The parser will take the leftmost non-terminal (**A**) and perform the possible syntactic derivation until it reaches a terminal symbol, as seen with `aa`. Then, it will continue with **B** and repeat the process, until all non-terminals have been derived. As we can observe, the parsing flow goes from top to bottom and from left to right (**Top-Down, Left-to-Right**).

To build an **LL(1)** parser (i.e., **Top-Down** with **1 lookahead**), the following rules must be satisfied:

- **No ambiguities**: A production rule cannot have identical symbols in its **First** sets:

$$S \to  iaT | ieT\\newline$$
$$First(iaT)={i}\\newline$$
$$First(ieT)={i}\\newline$$
  

- **No left recursion**: Left recursion must be avoided, as it creates an infinite loop when computing the **First** and **Follow** sets:

$$S \to  Sa \\newline$$

- **No non-determinism**: Non-deterministic rules are not allowed, because the parser can only use **one lookahead symbol** to decide:

$$S \to  aA |aB \\newline$$
$$A \to  d \\newline$$
$$B \to  c \\newline$$

In this case, both productions of **S** start with the terminal `a`, so the parser cannot decide deterministically.

### Code for Developing It: Algorithm Flow for Building an LL(1) Parser💻

- Construction of the LL(1) Table, with Non-Terminals as Rows and Terminals as Columns
```
#Implementation of the function to construct the LL(1) table
def LLTableConstruction(diccFirst, diccFollow,rule):
    #If the first of the rule has the first character, create the dictionary with the tuple of the follows of the production symbol of the rule.
    if "e" in rule.get_first():
        for i in range(len(diccFollow[rule.get_production_symbol()])):
            parsingTableLL[(rule.get_production_symbol(), diccFollow[rule.get_production_symbol()][i])] = rule.get_production()
    else:
        #Create the dictionary with the tuple of the production symbol of the rule, its first, and the production.
        for i in range(len(rule.get_first())):
            parsingTableLL[(rule.get_production_symbol(), rule.get_first()[i])] = rule.get_production()
```

The LLTableConstruction function builds the LL(1) parsing table, where rows represent non-terminal symbols and columns represent terminal symbols. For each rule, if the First set of the production contains epsilon (e), the function uses the Follow set of the non-terminal to fill the table. Otherwise, it uses each symbol in the First set to map the rule's production into the table. This process ensures that the LL(1) table is correctly populated for predictive parsing.

- String Validation in LL(1) Parsing Using Stack-Based Processing
  
```
#Process of validating a string using SLR.
def processLL(string,flagProcessLL):
     # Acceptance case: If the stack contains the value "4" and the string is the end symbol '$', the process ends successfully.
    if stackLL[-1] == "$" and string == "$":
        #Empty the stack and add the process to the history.
        stackLL.pop(0) 
        createHistoriesLL(stackLL,string)
        flagProcessLL = True
        return flagProcessLL
    #If the last symbol of the stack matches the first symbol of the string, perform a match and remove the processed symbols. 
    if stackLL[-1] == string[0]:
        string = string[1:]
        stackLL.pop(-1)
        createHistoriesLL(stackLL,string)
        return processLL(string,flagProcessLL)  #Performs recursion to continue processing the string.
    else:
        #Try to get the new symbols for the stack, which are the result of matching the last symbol of the stack and the character from the string to process.
        try:
            addStack = parsingTableLL[stackLL[-1],string[0]]
        except KeyError:
            return flagProcessLL
        stackLL.pop(-1) #Remove the symbol taken by the matching.
        addStack=addStack[::-1] #Invert the result to be entered into the stack.
        stackLL.extend(addStack) #Add this variable to the stack.
        #If an epsilon is added to the queue, it should be removed, as it represents the empty string.
        if addStack[-1] == "e":
            stackLL.pop(-1)
            createHistoriesLL(stackLL,string)
            return processLL(string,flagProcessLL)
        else:
            createHistoriesLL(stackLL,string)
            return processLL(string,flagProcessLL) #Performs recursion to continue processing the string.

#Add to the variables the respective history obtained in processedLL.
def createHistoriesLL(stackSLRSymbol,inputSymbol):
    inputHistory.append(inputSymbol)
    stackSLRHistory.append(list(stackSLRSymbol)[::-1])
```
The LL(1) parser validates input strings using a stack and a parsing table. It compares the top of the stack with the current input symbol: if they match, both are consumed; otherwise, the parser looks up the appropriate production in the LL(1) table to expand the non-terminal. This process continues recursively until the string is accepted or rejected.

- Print the process of parsing a string"
```
#Function to print the syntax analysis process.
def print_parsing_process_LL(stackSLRHistory, inputHistory, resutlLL):
    #Crear DataFrame
    df = pd.DataFrame({    "Stack": [" ".join(stack) for stack in stackSLRHistory],
    "Input": [" ".join(cadena) for cadena in inputHistory]})
    #Replace empty cells with '-'.
    df.replace('', '-', inplace=True)

    if resutlLL:
        resultado = "Cadena aceptada"
    else:
        resultado = "Cadena rechazada"
    df.loc[len(df.index)] = [resultado, "-----"]

    print(df.to_markdown(tablefmt="grid"))
```
This function prints the syntax analysis process of an LL(1) parser. It creates a DataFrame using the history of the stack and input symbols, displaying them step by step. If the string is accepted, it shows "Cadena aceptada" (String accepted); if rejected, it shows "Cadena rechazada" (String rejected). Empty cells in the table are replaced with dashes ('-'). The result is printed in a markdown table format for better visualization.

---

## SLR(1) Bottom-Up Parser 🔽

### Explanation of the Parser 📚

The SLR (Simple LR) parser is a **bottom-up** parsing method that processes the input **left to right**, constructing the parse tree **from bottom to top**. It uses **one lookahead symbol** to decide which production rule to apply or whether to reduce a production. The SLR parser is more powerful than the LL(1) parser because it can handle a broader range of grammars, including some that are not suitable for LL(1) parsing, but it still relies on a single lookahead symbol to make parsing decisions.

$$
\begin{array}{c}
         S \\
       / | \ \\
      a\ B\ x \\
     |\\
     aa\ \ \ 
\end{array}
$$

In an SLR parser, the approach is bottom-up, where the parser reads the input left to right, but instead of constructing the parse tree from top to bottom, it reduces the input string to the start symbol, working from the terminals upwards.

In the given example, we start with the input string aa and attempt to reduce it step by step. The first step is to find the rightmost matching production in the grammar and apply it. If we have a rule like:

$$S \to  aBx \\newline$$
And the current input is aa, the parser starts by identifying that the substring a can be reduced according to the production rule for B, eventually reducing the string down to S. Each step in the reduction process involves finding the leftmost matching production to replace the current sequence of symbols.The process works from the bottom to the top, where each non-terminal is reduced based on the lookahead symbol until the start symbol is reached, which indicates the acceptance of the string. Thus, the flow is bottom-up, with the parsing happening from left to right while reducing and constructing the parse tree.

- **No ambiguities**: A production rule cannot have identical symbols in its **First** sets:

$$S \to  iaT | ieT\\newline$$
$$First(iaT)={i}\\newline$$
$$First(ieT)={i}\\newline$$

- **No non-determinism**: Non-deterministic rules are not allowed, because the parser can only use **one lookahead symbol** to decide:

$$S \to  aA |aB \\newline$$
$$A \to  d \\newline$$
$$B \to  c \\newline$$

### Code for Developing It:  Algorithm Flow for Building an SLR(1) Parser🧑‍💻

This code implements the creation of LR(0) states for an SLR parser. It starts from an initial state and, by shifting the dot (.) over the productions, generates new states based on the symbol that appears after the dot. If a set of moved rules already exists, it reuses the corresponding state number; otherwise, it creates a new state. If the transition symbol is a terminal, a shift action is added to the SLR parsing table. If it's a non-terminal, a goto transition is recorded. It also handles reductions when the next symbol is ε (epsilon).

```
def createStateSRL(state):
    #Define the global variable 'numberState' to keep track of the states.
    global numberState
    stackStates = []
    stackStates.append(state)
    i = 0
    SLRStates = []
    #Iterate through the list of states until there are no more states to process.
    while not stackStates == []:
        #Take the first state from the list of states.
        stateActual = stackStates.pop(0)
        productions = stateActual.get_set_rules().copy()
        #We iterate through the list of productions to process each production.
        while i < len(productions):
            #We get the position of the dot in the production.
            dotPosition = productions[i].get_production().index(".")
            #If the dot is at the end of the production, it is considered a reduction and the productions are removed.
            if dotPosition == len(productions[i].get_production())-1:
                productions.remove(productions[i])
            else:
                #If the dot is not at the end, the symbol following the dot is obtained.
                symbolTransition = productions[i].get_production()[dotPosition+1]
                #All the productions that can be moved with that symbol are searched.
                listnext = identify_dot(productions,symbolTransition)
                movedDots = []
                rulesMoved = []
                #Move the dot in the productions that can be moved.
                for pm in range(len(listnext)):
                    movedDots.extend(movedot(listnext[pm]))
                #We keep track of the movements made (useful for avoiding duplicates and assigning shifts).
                for j in movedDots:
                    rulesMoved.append([j.get_production_symbol(),j.get_production()])
                #If the transition symbol is an e, we directly create a reduction in the table.
                if symbolTransition == "e":
                    for k in rules:
                        if symbolTransition == k.get_production():
                            for l in diccFollow[k.get_production_symbol()]:
                                if (stateActual.get_number_state(), l) not in parsingTableSLR:
                                    parsingTableSLR[(stateActual.get_number_state(),l)] = f"r{rules.index(k)}"
                #We search if the moved rules are already in the list of completed movements.
                #If they are, the corresponding state number is assigned for the shift.
                if  any(set(tuple(r) for r in rulesMoved) == set(tuple(r) for r in movement[1]) for movement in movementsCompleted):
                    for movement in movementsCompleted:
                        if set(tuple(r) for r in rulesMoved) == set(tuple(r) for r in movement[1]):
                            numberStatePrevious = movement[0]
                            break
                    #If the transition symbol is a non-terminal, the state number is assigned directly.
                    #If not, a shift is assigned in the parsing table.
                    if symbolTransition in nonTerminals:
                        parsingTableSLR[(stateActual.get_number_state(), symbolTransition)] = numberStatePrevious
                    else:
                        parsingTableSLR[(stateActual.get_number_state(), symbolTransition)] = f"d{numberStatePrevious}"
                else:
                    #If the movement is not found, a new state is created with the corresponding state number.
                    #The transition symbol is assigned and added to the list of completed movements.
                    newState = State(numberState,movedDots)
                    movementsCompleted.append([numberState,rulesMoved])
                    newState.set_previus_state(stateActual.get_number_state())
                    newState.set_symbol(symbolTransition)
                    SLRStates.append(newState)
                    stackStates.append(newState)
                    numberState+=1
    return SLRStates
```

-Search for the rules that have a given production symbol:
```
#Search for the rules that have a given production symbol.
def searchRules(rules, symbol):
    listReturn = []
    #Iterate over all the rules to find matches with the production symbol.
    for i in rules:
        if i.get_production_symbol() == symbol:
            #Create a new rule with the dot at the beginning of the production.
            x = Rule(symbol,"."+i.get_production())
            #If the second symbol of the production is a non-terminal, add the rule and search for more rules recursively.
            if x.get_production()[1] in nonTerminals:
                listReturn.append(x)
                if i.get_production()[0] != symbol:
                    listReturn.extend(searchRules(rules, x.get_production()[1]))
            else:
                #Being a terminal, it only adds the rule, as it does not generate a transition to another.
                listReturn.append(x)
    return listReturn
```
- Identify dot in each production
```
def identify_dot(productions, symbolTransition):
    rulesRight = []
    #Iterate over all the productions to find those that have a dot before 'symbolTransition.
    for i in productions:
        positionNonTerminal = i.get_production().index(".")
        #Check if the dot is not at the end and if the next symbol is the transition one.
        if positionNonTerminal < len(i.get_production())-1:
            if i.get_production()[positionNonTerminal+1] == symbolTransition:
                rulesRight.append(i)
    #Remove the rules that have been added to 'rulesRight' from the list of productions.
    for i in rulesRight:
        productions.remove(i)
    #Return the list of rules that match the symbol transition.
    return rulesRight
```
- Move dot in each production
```
def movedot(rule):
    listrules = []
    #Get the production of the rule and locate the dot in the production.
    production = rule.get_production()
    dotPosition = rule.get_production().index(".")
    #Create a new production by moving the dot one position forward.
    newProduction = production[:dotPosition] + production[dotPosition+1] + "." + production[dotPosition+2:]
    #Try to find the new symbol after the dot and search for more rules recursively if it is a non-terminal
    try:
        dotPosition = newProduction.index(".")
        newSymbol = newProduction[dotPosition + 1]
        if newSymbol in nonTerminals:
            listrules.extend(searchRules(rules,newSymbol))
    except ValueError:
        #If no dot is found, None is assigned to the new symbol.
        newSymbol = None
    except IndexError:
        #If the index is out of range, None is assigned to the new symbol.
        newSymbol = None
    #Create a new rule with the modified production and add it to the list of rules that make up each state.
    newRule = Rule(rule.get_production_symbol(),newProduction)
    listrules.append(newRule)
    return listrules
```


This code constructs the **SLR parsing table** by analyzing the states generated by the LR(0) automaton. It iterates through each transition and, depending on whether the symbol is a **terminal or non-terminal**, it adds an action (shift or transition) to the parsing table. It also identifies the rules where the **dot is at the end of the production** to generate **reduction actions**, based on the **Follow set** of the corresponding non-terminal. If an action already exists in the table cell, ambiguity is detected and `flagSLR` is set to `False`.

```
def SLRTableConstruction(diccFollow, listStatesResultant):
    global flagSLR
    # Iterates over each state in the list of resulting states.
    for i in listStatesResultant:
        # If the symbol is a non-terminal, a transition or action is added to the parsing table.
        if i.get_symbol() in nonTerminals:
            # If the symbol is a non-terminal, the state number is assigned directly.
            if (i.get_previus_state(), i.get_symbol()) not in parsingTableSLR:
                parsingTableSLR[(i.get_previus_state(), i.get_symbol())] = i.get_number_state()
            # If the transition already exists (i.e., there is already a shift or action for that state and symbol), it is marked as ambiguity.
            else:
                flagSLR = False
        else:
            # If the symbol is a terminal, a shift is added to the parsing table.
            if (i.get_previus_state(), i.get_symbol()) not in parsingTableSLR:
                parsingTableSLR[(i.get_previus_state(), i.get_symbol())] = f"d{i.get_number_state()}"
            else:
            # If the transition already exists (i.e., there is already a shift or action for that state and symbol), it is marked as ambiguity.
                flagSLR = False

        #We start reviewing the rules that have the dot at the end of the production.
        for j in i.get_set_rules():
            if j.get_production()[-1] == ".":
                ruleFinal = j.get_production().rstrip(".")
                for k in rules:
                    if ruleFinal == k.get_production():
                        #If the production is equal to the rule, a reduction action is created with the index of it.
                        for l in diccFollow[k.get_production_symbol()]:
                            if (i.get_number_state(), l) not in parsingTableSLR:
                                parsingTableSLR[(i.get_number_state(),l)] = f"r{rules.index(k)}"
                            # If the action already exists (i.e., there is already a shift or action for that state and symbol), it is marked as ambiguity.
                            else:
                                print(f"Ambiguity in the State {i.get_number_state()} with the rule {k.get_production_symbol()} -> {k.get_production()}")
                                flagSLR = False
```
This code snippet implements the SLR string validation process. The algorithm starts with a parsing stack and an input string. At each step, it checks the SLR parsing table using the current top state of the stack and the first symbol of the input. If it finds a shift action, it consumes the symbol, adds it to the list of processed symbols, updates the stack with the new state, and continues recursively. The process successfully ends if it reaches an accepting state (state 1 and symbol $). If no valid action is found, the string is rejected.

```
#Process of validating a string using SLR.
def processSLR (string,stackSLR,processedSymbols,flagProcessSLR):
    # Acceptance case: If the stack contains the value 1 and the string is the end symbol '$', the process ends successfully.
    if stackSLR[-1] == 1 and string == "$":
        flagProcessSLR = True
        return flagProcessSLR
    # Try to get the action from the SLR parsing dictionary using the stack and the first symbol of the string.
    try:
        action = parsingTableSLR[stackSLR[-1],string[0]]
    except KeyError:
        #If not found, return the flag that controls the validation, meaning the string does not belong to the language.
        return flagProcessSLR
    
    #Check if the action is a shift.
    if action[0] == "d":
            #Being a shift, the character being processed will be added to processedSymbols, as it has been read.
            processedSymbols.append(string[0])
            newString = string[1:] #Remove the shifted character from processedSymbols from the string to process.
            stackSLR.append(int(action[1:])) #Add the action to the processing stack.
            createHistoriesSLR(action,stackSLR,newString,processedSymbols)
            return processSLR(newString,stackSLR,processedSymbols,flagProcessSLR) 
```

```
def createHistoriesSLR(actionSymbol,stackSLRSymbol,inputSymbol,simbolsSymbol):
    actionHistory.append(actionSymbol)
    symbolHistory.append(list(simbolsSymbol))
    inputHistory.append(inputSymbol)
    stackSLRHistory.append(list(stackSLRSymbol))
```


## General Code

We import the necessary libraries to ensure the proper functioning of the program, including tools for data handling and graph generation such as pandas and graphviz.

```
from graphviz import Diagraph
import pandas as pd
from Rule import Rule
from State import State
```
We define a function to display information in a table format using pandas, which helps visualize parsing tables or grammars in a clear and structured way.
```
def print_parsing_table(parsingTable):
    #rows y columns
    rows = sorted({k[0] for k in parsingTable})
    columns = sorted({k[1] for k in parsingTable})
    #Crear DataFrame
    df = pd.DataFrame('', index=rows, columns=columns)
    for (fila, col), valor in parsingTable.items():
        df.at[fila, col] = valor
    #Reemplazar celdas vacías con '-'
    df.replace('', '-', inplace=True)
    #Imprimir con líneas
    print(df.to_markdown(tablefmt="grid"))
```

We use Graphviz to display the syntactic derivation tree, allowing us to visually represent the structure of the parsed input based on the grammar rules.

```
def dibujar_arbol_LL(rules):
    dot = Digraph(comment='Árbol de Derivación')
    for i in range(len(rules)):
        print(rules[i].get_production_symbol(),rules[i].get_production())
        if rules[i].get_production_symbol() == startSymbolGrammar and i == 0:
            for j in range(len(rules[i].get_production())):
                idNodes.append(rules[i].get_production()[j]+"0")
        else:
            j=0
            symbol = rules[i].get_production_symbol()
            for j in range(len(idNodes)):
                try:
                    if symbol == idNodes[j][0]:
                        lastSymbolId = idNodes[j]
                        print("lastSymbolId",lastSymbolId)
                        if lastSymbolId not in idNodes:
                            idNodes.append(lastSymbolId)
                        break
                except IndexError:
                    break

            for j in range(len(rules[i].get_production())):
                flagTree=False
                symbolProductionId = rules[i].get_production()[j]
                for k in range(len(idNodes) - 1, -1, -1):
                    if symbolProductionId == idNodes[k][0]:
                        lastSymbolProduction = idNodes[k]
                        symbolProductionId = symbolProductionId + str(int(lastSymbolId[1:]) + 1)
                        idNodes.append(symbolProductionId)
                        flagTree=True
                        break
                if not flagTree:
                    idNodes.append(rules[i].get_production()[j]+"0")
    return idNodes


def print_tree_LL(derivationHistory, startSymbolGrammar):
    dot = Digraph(comment='Árbol de Derivación')
    derivacion = derivationHistory.copy()
    repeticion = {startSymbolGrammar: 0}
    actual = 0
    for i in derivacion:
        actual = repeticion[i[0]]
        for j in i[1]:
            if j in repeticion:
                repeticion[j] += 1
            else:
                repeticion[j] = 0
            dot.node(j+str(repeticion[j]), j)
            if j != i[0]:
                dot.edge(i[0]+str(actual), j+str(repeticion[j]))
            else:
                dot.edge(i[0]+str(actual), j+str(repeticion[j]))

    dot.render('arbol', view=True, format="png")  # Esto crea y abre el archivo
    print(repeticion)
    print(derivacion)
    print("--------------------------------------------------")
    #Nodos
```
