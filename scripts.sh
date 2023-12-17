# Add these to your ~/.bash_aliases
AOC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export AOC

function aoc () {
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo "Error: Two arguments required (year and day)."
        echo "Usage: aoc <year> <day>"
        return 1  # Exit with an error status
    fi

    local year=$1
    local day=$2

    printf "\033[0;34m"  # Set text color to blue
    aot "$year" "$day"
    printf "\033[0m"  # Reset text color
    echo
    aos "$year" "$day"
}

function aos () {
    local year=$1
    local day=$2
    local inputFile="$AOC/data/input-$year-$day.txt"
    local solutionFile="$AOC/solutions/$year/python/day-$day.py"

    if [ -f "$inputFile" ] && [ -f "$solutionFile" ]; then
        python3 "$solutionFile" < "$inputFile"
    else
        echo "Input file $inputFile or solution file $solutionFile not found."
        return 1
    fi
}

function aot () {
    local year=$1
    local day=$2
    local solutionFile="$AOC/solutions/$year/python/day-$day.py"
    local testFile="$AOC/data/test-$year-$day.txt"


    if [ -f "$solutionFile" ] && [ -f "$testFile" ]; then
        python3 "$solutionFile" < "$testFile"
    else
        echo "Solution file $solutionFile or test file $testFile not found."
        return 1
    fi
}

function aoc-load () {
    export $(cat .env | xargs)
    local inputFile
    local testFile
    local dataDir="$AOC/data"

    # Check if the data directory exists, fail if it does not
    if [ ! -d "$dataDir" ]; then
        echo "Error: Data directory $dataDir does not exist. Please create it and try again."
        return 1  # Exit the function with an error status
    fi

    if [ $1 ] && [ $2 ]
    then
        local YEAR=$1
        local DAY=$2
    else
        local YEAR=$(date +%Y)
        local DAY=$(date +%d | sed 's/^0//')  # Remove leading zero if any
    fi

    inputFile="$dataDir/input-$YEAR-$DAY.txt"
    testFile="$dataDir/test-$YEAR-$DAY.txt"

    # Check if the file already exists
    if [ -f "$inputFile" ]; then
        echo "File $inputFile already exists. Skipping download."
    else
        curl --cookie "session=$AOC_COOKIE" "https://adventofcode.com/$YEAR/day/$DAY/input" > "$inputFile"
        touch "$testFile"
    fi
}
