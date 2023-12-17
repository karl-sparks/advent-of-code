# Add these to your ~/.bash_aliases

alias aos="python3 solution.py < data/in.txt"
alias aot="cd $AOC; echo -ne '\\e[0;34m'; python3 solution.py < test.txt; echo -ne '\\e[0m'"
alias aoc="aot; echo; aos"

function aos () {
    local year=$1
    local day=$2
    local inputFile="$AOC/data/input-$year-$day.txt"

    if [ -f "$inputFile" ]; then
        python3 solution.py < "$inputFile"
    else
        echo "Input file $inputFile not found."
        return 1
    fi
}

function aoc-load () {
    export $(cat .env | xargs)
    local inputFile
    local dataDir="$AOC/data"

    # Check if the data directory exists, fail if it does not
    if [ ! -d "$dataDir" ]; then
        echo "Error: Data directory $dataDir does not exist. Please create it and try again."
        return 1  # Exit the function with an error status
    fi

    if [ $1 ] && [ $2 ]
    then
        inputFile="$dataDir/input-$1-$2.txt"
    else
        local YEAR=$(date +%Y)
        local DAY=$(date +%d | sed 's/^0//')  # Remove leading zero if any
        inputFile="$dataDir/input-$YEAR-$DAY.txt"
    fi

    # Check if the file already exists
    if [ -f "$inputFile" ]; then
        echo "File $inputFile already exists. Skipping download."
    else
        # Download the file if it doesn't exist
        if [ $1 ] && [ $2 ]
        then
            curl --cookie "session=$AOC_COOKIE" "https://adventofcode.com/$1/day/$2/input" > "$inputFile"
        else
            curl --cookie "session=$AOC_COOKIE" "$(echo `date +https://adventofcode.com/%Y/day/%d/input` | sed 's/\/0/\//g')" > "$inputFile"
        fi
    fi
}
