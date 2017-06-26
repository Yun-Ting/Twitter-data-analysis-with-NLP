class Dog:
	name = ''
	breed = ''
	large_dogs = [
		'German Shepherd', 
		'Golden Retriever',
		'Rottweiler',
		'Collie',
		'Mastiff',
		'Great Dane']
	small_dogs = [
		'Lhasa Apso',
		'Yorkshire Terrier',
        'Beagle', 'Dachshund', 'Shih Tzu']

    def __init__(self, nm, br):
    	self.name = nm
    	self.breed = br

    def speak(self):
    	if self.breed in self.large_dogs:
    		print ('woof')
    	elif self.breed in self.small_dogs:
    		print ('yip')
    	else:
    		print ('rrrrr')


d1 = Dog('Fido', 'German Shepherd')
d2 = Dog('Rufus', 'Lhasa Apso')
d3 = Dog('Fred', 'Mutt')

d1.speak()
d2.speak()
d3.speak()
