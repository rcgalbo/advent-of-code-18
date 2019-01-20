from typing import Dict, List

n_in = 540391
test_recipe = [int(i) for i in list('37')]

def get_new_recipe(elf: Dict[str, int], recipe: List[int]) -> Dict[str, int]:
    elf['val'] = recipe[elf['ind']]
    return elf

elf1 = {'ind': 0}
elf2 = {'ind': 1}
elfs = [elf1,elf2]
for elf in elfs: elf = get_new_recipe(elf,test_recipe)


def next_recipe(elfs: List[Dict[str, int]], recipe: List[int]):

    next_recipe = sum(elf['val'] for elf in elfs)
    recipe += [int(i) for i in list(str(next_recipe))]

    for elf in elfs:
        elf['ind'] = ((elf['val'] + 1) + elf['ind']) % len(recipe)
        elf['val'] = recipe[elf['ind']]

    return recipe, elfs
    
def get_next_n(recipe, elfs, n= 10):
    for _ in range(n+10):
        recipe, elfs = next_recipe(elfs, recipe)
    return recipe[n:n+10]

# for elf in elfs:
#     elf = get_new_recipe(elf,test_recipe)
# test = get_next_n(test_recipe, elfs)
# print(test)

# part 1
new = get_next_n(test_recipe,elfs,n=n_in)
print(''.join(str(x) for x in new))

# part 2

def next_recipe(elfs: List[Dict[str, int]], recipe: List[int]):

    next_recipe = sum(elf['val'] for elf in elfs)
    str_new = str(next_recipe)
    recipe.extend(divmod(next_recipe, 10) if next_recipe >= 10 else (next_recipe,))

    for elf in elfs:
        elf['ind'] = ((elf['val'] + 1) + elf['ind']) % len(recipe)
        elf['val'] = recipe[elf['ind']]

    return recipe, elfs, str_new

recipe = test_recipe
recipe_str = ''.join(str(i) for i in recipe)
pattern = str(n_in)
while recipe_str[-7:].find(pattern) < 0:
    recipe, elfs, str_new = next_recipe(elfs, recipe)
    recipe_str = recipe_str + str_new
    

print(recipe_str.find(pattern))
    


