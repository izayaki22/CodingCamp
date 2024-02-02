import argparse
import logging
import os

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.optim import Adam
from torchvision import transforms as T
from tqdm import tqdm

from dataset import FoodDataset
from model import vanillaCNN, vanillaCNN2, VGG19

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', type=str, choices=['CNN1', 'CNN2', 'VGG'], required=True, help='model architecture to train')
    parser.add_argument('-e', '--epoch', type=int, default=100, help='the number of train epochs')
    parser.add_argument('-b', '--batch', type=int, default=32, help='batch size')
    parser.add_argument('-lr', '--learning_rate', type=float, default=1e-4, help='learning rate')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    
    os.makedirs('./save', exist_ok=True)
    os.makedirs(f'./save/{args.model}_{args.epoch}_{args.batch}_{args.learning_rate}', exist_ok=True)
    
    transforms = T.Compose([
        T.Resize((227,227), interpolation=T.InterpolationMode.BILINEAR),
        T.RandomVerticalFlip(0.5),
        T.RandomHorizontalFlip(0.5),
        T.ToTensor()
    ])

    train_dataset = FoodDataset("./data", "train", transforms=transforms)
    train_loader = DataLoader(train_dataset, batch_size=args.batch, shuffle=True)
    val_dataset = FoodDataset("./data", "val", transforms=transforms)
    val_loader = DataLoader(val_dataset, batch_size=args.batch, shuffle=True)
    
    if torch.cuda.is_available():
        device = torch.device('cuda')
    elif torch.backends.mps.is_available():
        device = torch.device('mps')
    else:
        device = torch.device('cpu')
    
    if args.model == 'CNN1':
        model = vanillaCNN()
    elif args.model == 'CNN2':
        model = vanillaCNN2()
    elif args.model == 'VGG': 
        model = VGG19()
    else:
        raise ValueError("model not supported")
        
    ##########################   fill here   ###########################
        
    # TODO : Training Loop을 작성해주세요
    # 1. logger, optimizer, criterion(loss function)을 정의합니다.
    # train loader는 training에 val loader는 epoch 성능 측정에 사용됩니다.
    # torch.save()를 이용해 epoch마다 model이 저장되도록 해 주세요
            
    ######################################################################
    logging.basicConfig(filename='./logs/log1.txt', level = logging.INFO, format = '(%(asctime)s) : %(levelname)s : %(message)s', filemode='w')
    logger = logging.getLogger(__name__)

    model.to(device)
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr = args.learning_rate)
    
    max_val = 0
    max_ep = 0
    
    for ep in range(args.epoch):
        
        logging.info(f'training epoch {ep}')
        
        model.train()
        loss_sum = 0
        
        for batch, (image, label) in enumerate(tqdm(train_loader)):
            
            image = image.to(device)
            label = label.to(device)
            
            pred = model(image)
            loss = criterion(pred, label)
            
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            
            loss_sum += loss.item()
            logging.debug(f'Step {batch} loss : {loss.item()}')
            
        logging.info(f'Epoch {ep} loss : {loss_sum / (batch + 1)}')
        
        logging.info(f'Validating epoch {ep}')
            
        model.eval()
        total = 0
        correct = 0
        
        with torch.no_grad():
           for (image, label) in tqdm(val_loader):
                
                total += len(image)
                
                image = image.to(device)
                label = label.to(device)
                
                pred = model(image)
                _, indices = torch.max(pred, dim = 1)
                
                correct += (indices == label).sum().item()
        
        accuracy = correct / total
        logging.info(f'Epoch {ep} accuracy = {accuracy}')
        torch.save(model.state_dict(), f'./save/{args.model}_{args.epoch}_{args.batch}_{args.learning_rate}/{ep}_score: {accuracy : .3f}.pth')
        
        if(max_val < accuracy):
            max_val = accuracy
            max_ep = ep
    
    print(f"Best validation score is: {max_val} and epoch is {max_ep}")        
            

