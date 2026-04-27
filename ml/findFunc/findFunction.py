# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 21:10:09 2021

@author: Xela
"""


import torch
from torch import nn, tensor
torch.manual_seed(242)

from itertools import product


from os import environ
environ["KMP_DUPLICATE_LIB_OK"]="TRUE" #otherwise things go bad



import math
from math import sin, cos, pi, e, exp

from random import uniform

from numpy import arange



import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
#to go back to visible plotting use
#%matplotlib inline

from tqdm import tqdm

from imageio import imread, mimsave

from datetime import datetime



def f(x):
    return sin(x)

lowerBound = -1*pi
upperBound = 1*pi

trainData = []
for i in range(96):
   x = uniform(lowerBound, upperBound)
   trainData.append([x, f(x)])

#trainData = [[float(x), float(f(x))] for x in arange(-1*pi, pi, .08)]

trainData = tensor(trainData)

dataLength = len(trainData)

#requires trainLabels, but GAN doesn't use them
trainLabels = torch.zeros(dataLength)

trainSet = [

    (trainData[i], trainLabels[i]) for i in range(dataLength)

]



batchSize = 6
trainLoader = torch.utils.data.DataLoader(trainSet, batchSize, shuffle=True)


#discriminator:
class Discriminator(nn.Module):
   def __init__(self):
      super().__init__()
      self.model = nn.Sequential(
         nn.Linear(2, 1024), #2 is inDimension
         nn.ReLU(), #ReLU is the activatoin function of a neuron
         nn.Dropout(.3), #fancy way to avoid overfit

         nn.Linear(1024, 512), #dimensions of input are the output neurons of the previous layer
         nn.ReLU(),
         nn.Dropout(.3),

         nn.Linear(512, 256),
         nn.ReLU(),
         nn.Dropout(.3),

         nn.Linear(256, 128),
         nn.ReLU(),
         nn.Dropout(.3),

         nn.Linear(128, 64),
         nn.ReLU(),
         nn.Dropout(.3),

         nn.Linear(64, 1),

         nn.Sigmoid(), #using sigmoid turns it into a probability
      )

   def forward(self, x): #how is the output calculated
      #x is the input to the model

      output = self.model(x) #just pass the input to the model
      return output


class Generator(nn.Module):
   def __init__(self):
      super().__init__()
      self.model = nn.Sequential(
         nn.Linear(1, 16), #dim
         nn.ReLU(),

         nn.Linear(16, 32),
         nn.ReLU(),

         nn.Linear(32, 64),
         nn.ReLU(),

         nn.Linear(64, 128),
         nn.ReLU(),

         nn.Linear(128, 256),
         nn.ReLU(),

         nn.Linear(256, 512),
         nn.ReLU(),

         nn.Linear(512, 1024),
         nn.ReLU(),

         nn.Linear(1024, 1), #dim

      )

   def forward(self, x):
      output = torch.stack( (x, self.model(x)), dim=1)[:, :, 0]

      return output


discriminator = Discriminator()
generator = Generator()

lr = .001 #lr is learning rate
lossFunction = nn.BCELoss() #a loss function. idk what bce loss is. it works for binary discriminators.


optimizerDiscriminator = torch.optim.Adam(discriminator.parameters(), lr=lr)
optimizerGenerator = torch.optim.Adam(generator.parameters(), lr=lr)

step = .1
fixedLatentSpace = tensor([ [float(x)] for x in arange(lowerBound, upperBound, step) ])

def train(epochs, lr=lr, plot=True):
   #training loop:
   for epoch in tqdm(epochs):
      for n, (realSamples, _) in enumerate(trainLoader):
         # Data for training the discriminator

         realSamplesLabels = torch.ones((batchSize, 1))

         latentSpaceSamples = torch.randn(batchSize, 1) #dim

         generatedSamples = generator(latentSpaceSamples)

         generatedSamplesLabels = torch.zeros((batchSize, 1))

         allSamples = torch.cat(

            (realSamples, generatedSamples)

            )

         allSamplesLabels = torch.cat(

             (realSamplesLabels, generatedSamplesLabels)

         )


         # Training the discriminator

         discriminator.zero_grad() #need to clear grads at every step

         outputDiscriminator = discriminator(allSamples)

         lossDiscriminator = lossFunction(

             outputDiscriminator, allSamplesLabels) #compare discrim with the label

         lossDiscriminator.backward() #calculate the grads

         optimizerDiscriminator.step() #update the weights using the grads


         # Data for training the generator
         latentSpaceSamples = torch.randn(batchSize, 1) #dim

         # Training the generator

         generator.zero_grad()

         generatedSamples = generator(latentSpaceSamples)

         outputDiscriminatorGenerated = discriminator(generatedSamples)

         lossGenerator = lossFunction(

             outputDiscriminatorGenerated, realSamplesLabels

         )

         lossGenerator.backward()

         optimizerGenerator.step()



      #end of the for n loop, now in for epoch loop

      #decay lr to stabilize over time
      if epoch < 250:
         lr *= .985
      else:
         lr *= .998

      for param_group in optimizerDiscriminator.param_groups:
         param_group['lr'] = lr

      for param_group in optimizerGenerator.param_groups:
         param_group['lr'] = lr


      #plot stuff
      if plot:
         generatedSamples = generator(fixedLatentSpace).detach()

         plt.figure(epoch + 1)
         plt.title('Epoch%s' % epoch)

         plt.plot(trainData[:,0], trainData[:, 1], '.')
         plt.plot(generatedSamples[:, 0], generatedSamples[:, 1], '.')

         plt.savefig('epochs/epoch%s' % epoch)
         plt.close()

   return lr


#gif functions
def trainingGif(epochs, timestamp=''):
   tqdm.write("\nLoading gif frames...")
   images = []
   for epoch in tqdm(range(0, epochs[-1])):
      images.append(imread('epochs/epoch%s.png' % epoch))


   mimsave('training-%s.gif' % timestamp, images)



def latentMapGif(bounds, timestamp=''): #bounds: [ [lowX, highX, step], [lowY, highY, step] ]
   latentPoints = []
   for x, y in product( arange(*bounds[0]), arange(*bounds[1]) ):
      latentPoints.append([x, y])

   generatedPoints = generator(tensor(latentPoints).float()).detach()

   print('\nMaking latentMapGif...')
   i=0
   for (latentPoint, generatedPoint) in tqdm(list(zip(latentPoints, generatedPoints))):
      plt.figure('latentMap%s' % i)


      plt.subplot(211, label="Latent Points")
      plt.plot(latentPoint[0], latentPoint[1], '.')
      plt.xlim(*bounds[0][0:2])
      plt.ylim(*bounds[1][0:2])

      plt.subplot(212, label="Generated Points")
      plt.plot(generatedPoint[0], generatedPoint[1], '.')
      plt.xlim(*bounds[0][0:2])
      plt.ylim(*bounds[1][0:2])


      plt.savefig('latentMapPoints/latentMap%s' % i)

      plt.close()

      i += 1


   tqdm.write("\nLoading gif frames...")
   images = []
   for i in tqdm(range(i)):
      images.append(imread('latentMapPoints/latentMap%s.png' % i))

   mimsave('latentMapGif-%s.gif' % timestamp, images, subrectangles=True)



xBound = [lowerBound, upperBound, step]
yBound = [-1, 1, step]
trainingPlotBounds = [xBound, yBound]

def main(epochs, lr=lr, plot=True, trainingPlotBounds=trainingPlotBounds, latentSpaceBounds=None):
   lr = train(epochs, lr=lr, plot=plot)

   now = str(datetime.now()).replace(':', '-').replace('.', '-')

   if plot:
      trainingGif(epochs, now)

   if latentSpaceBounds:
      latentMapGif(latentSpaceBounds, now)


   return lr

#note: epochs is a range

bounds=[ [-1*math.pi, math.pi, .5], [-1, 1, .5] ]


main(range(100), plot=True, latentSpaceBounds=bounds)
#to save: torch.save(model, 'filename.zip')
#to load: torch.load(model, 'filename.zip')