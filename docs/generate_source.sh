GREEN='\033[0;32m'
YELLOW='\033[1;33m'
GRAY='\033[0;37m'

NC='\033[0m' # No Color

echo -e "${GREEN}Generating the RST files ${GRAY}"
python ./generate_modules.py ../EDA_miner -n "EDA Miner" -f -s rst -d source > /dev/null
echo -e "${GREEN}Building the SPHINX${GRAY}"
echo -e "${YELLOW}Cleaning build directory${GRAY}"
make clean
echo -e "${YELLOW}Generating new html${GRAY}"
make html
echo -e "${GREEN}Replacing index.html with models.html${GRAY}"
cp ./build/html/modules.html ./build/html/index.html
